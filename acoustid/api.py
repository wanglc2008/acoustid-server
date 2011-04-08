# Copyright (C) 2011 Lukas Lalinsky
# Distributed under the MIT license, see the LICENSE file for details. 

from acoustid.handler import Handler, Response
from acoustid.track import lookup_mbids
from acoustid.musicbrainz import lookup_metadata
from acoustid.submission import insert_submission
from acoustid.fingerprintdata import FingerprintData
from werkzeug.exceptions import HTTPException
import xml.etree.cElementTree as etree
import chromaprint


def xml_response(elem, **kwargs):
    xml = etree.tostring(elem, encoding="UTF-8")
    return Response(xml, content_type='text/xml')


def error_response(error):
    root = etree.Element('response', status='error')
    etree.SubElement(root, 'error').text = error
    return xml_response(root, status=400)


class BadRequest(HTTPException):

    code = 400

    def get_response(self, environ):
        return error_response(self.description)


class MissingArgument(BadRequest):

    def __init__(self, name):
        description = "Missing argument '%s'" % (name,)
        BadRequest.__init__(self, description)


class LookupHandler(Handler):

    def __init__(self, conn, fingerprint_data):
        self.conn = conn
        self.fingerprint_data = fingerprint_data

    def _inject_metadata(self, meta, result_map):
        track_mbid_map = lookup_mbids(self.conn, result_map.keys())
        if meta > 1:
            all_mbids = []
            for track_id, mbids in track_mbid_map.iteritems():
                all_mbids.extend(mbids)
            track_meta_map = lookup_metadata(self.conn, all_mbids)
        for track_id, mbids in track_mbid_map.iteritems():
            result = result_map[track_id]
            tracks = etree.SubElement(result, 'tracks')
            for mbid in mbids:
                track = etree.SubElement(tracks, 'track')
                etree.SubElement(track, 'id').text = str(mbid)
                if meta == 1:
                    continue
                track_meta = track_meta_map[mbid]
                etree.SubElement(track, 'name').text = track_meta['name']
                artist = etree.SubElement(track, 'artist')
                etree.SubElement(artist, 'id').text = track_meta['artist_id']
                etree.SubElement(artist, 'name').text = track_meta['artist_name']

    def handle(self, req):
        fingerprint_string = req.args.get('fingerprint')
        if not fingerprint_string:
            raise MissingArgument('fingerprint')
        fingerprint, version = chromaprint.decode_fingerprint(fingerprint_string)
        if version != 1:
            raise BadRequest('Unsupported fingerprint version')
        length = req.args.get('length', type=int)
        if not length:
            raise MissingArgument('length')
        meta = req.args.get('meta', type=int, default=0)
        root = etree.Element('response', status='ok')
        results = etree.SubElement(root, 'results')
        matches = self.fingerprint_data.search(fingerprint, length, 0.7, 0.3)
        result_map = {}
        for fingerprint_id, track_id, score in matches:
            if track_id in result_map:
                continue
            result_map[track_id] = result = etree.SubElement(results, 'result')
            etree.SubElement(result, 'id').text = str(track_id)
            etree.SubElement(result, 'score').text = '%.2f' % score
        if meta and result_map:
            self._inject_metadata(meta, result_map)
        return xml_response(root)

    @classmethod
    def create_from_server(cls, server):
        conn = server.engine.connect()
        return cls(conn, FingerprintData(conn))


def iter_args_suffixes(args, prefix):
    prefix_dot = prefix + '.'
    for name in args.iterkeys():
        if name == prefix:
            yield ''
        elif name.startswith(prefix_dot):
            prefix, suffix = name.split('.', 1)
            if suffix.isdigit():
                yield '.' + suffix

class SubmitHandler(Handler):

    def __init__(self, conn):
        self.conn = conn

    def _read_fp_params(self, args, suffix):
        def read_arg(name):
            if name + suffix in args:
                return args[name + suffix]
        p = {}
        p['puid'] = read_arg('puid')
        p['mbids'] = [read_arg('mbid')]
        p['length'] = read_arg('length')
        p['fingerprint'] = chromaprint.decode_fingerprint(read_arg('fingerprint'))[0]
        p['bitrate'] = read_arg('bitrate')
        p['format'] = read_arg('format')
        return p

    def handle(self, req):
        params = []
        for suffix in iter_args_suffixes(req.args, 'fingerprint'):
            params.append(self._read_fp_params(req.args, suffix))
        with self.conn.begin():
            for p in params:
                for mbid in p['mbids']:
                    insert_submission(self.conn, {
                        'mbid': mbid,
                        'puid': p['puid'],
                        'bitrate': p['bitrate'],
                        'fingerprint': p['fingerprint'],
                        'length': p['length']
                    })
        root = etree.Element('response', status='ok')
        return xml_response(root)

    @classmethod
    def create_from_server(cls, server):
        conn = server.engine.connect()
        return cls(conn)
