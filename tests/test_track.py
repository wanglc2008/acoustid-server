# Copyright (C) 2011 Lukas Lalinsky
# Distributed under the MIT license, see the LICENSE file for details. 

from nose.tools import *
from tests import prepare_database, with_database
from acoustid.track import merge_missing_mbids


@with_database
def test_merge_missing_mbids(conn):
    prepare_database(conn, """
INSERT INTO track (id) VALUES (1);
INSERT INTO track (id) VALUES (2);
INSERT INTO track (id) VALUES (3);
INSERT INTO track (id) VALUES (4);
INSERT INTO track_mbid (track_id, mbid) VALUES (1, '97edb73c-4dac-11e0-9096-0025225356f3');
INSERT INTO track_mbid (track_id, mbid) VALUES (1, 'b81f83ee-4da4-11e0-9ed8-0025225356f3');
INSERT INTO track_mbid (track_id, mbid) VALUES (1, 'd575d506-4da4-11e0-b951-0025225356f3');
INSERT INTO track_mbid (track_id, mbid) VALUES (2, 'd575d506-4da4-11e0-b951-0025225356f3');
INSERT INTO track_mbid (track_id, mbid) VALUES (3, '97edb73c-4dac-11e0-9096-0025225356f3');
INSERT INTO track_mbid (track_id, mbid) VALUES (4, '5d0290a6-4dad-11e0-a47a-0025225356f3');
INSERT INTO musicbrainz.artist (id, name, sortname, gid, page) VALUES
    (1, 'Artist A', 'Artist A', 'a64796c0-4da4-11e0-bf81-0025225356f3', 0);
INSERT INTO musicbrainz.track (id, artist, name, gid) VALUES
    (1, 1, 'Track A', 'b81f83ee-4da4-11e0-9ed8-0025225356f3'),
    (2, 1, 'Track B', '6d885000-4dad-11e0-98ed-0025225356f3');
INSERT INTO musicbrainz.gid_redirect (newid, gid, tbl) VALUES
    (1, 'd575d506-4da4-11e0-b951-0025225356f3', 3),
    (2, '5d0290a6-4dad-11e0-a47a-0025225356f3', 3),
    (99, 'b44dfb2a-4dad-11e0-bae4-0025225356f3', 2);
""")
    merge_missing_mbids(conn)
    rows = conn.execute("SELECT track_id, mbid FROM track_mbid ORDER BY track_id, mbid").fetchall()
    expected_rows = [
        (1, '97edb73c-4dac-11e0-9096-0025225356f3'),
        (1, 'b81f83ee-4da4-11e0-9ed8-0025225356f3'),
        (2, 'b81f83ee-4da4-11e0-9ed8-0025225356f3'),
        (3, '97edb73c-4dac-11e0-9096-0025225356f3'),
        (4, '6d885000-4dad-11e0-98ed-0025225356f3'),
    ]
    assert_equals(expected_rows, rows)