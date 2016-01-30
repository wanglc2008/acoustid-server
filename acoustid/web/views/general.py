import os
import markdown.util
from markdown import Markdown
from flask import Blueprint, render_template, current_app, redirect, url_for

general_page = Blueprint('general', __name__)


@general_page.route('/favicon.ico')
def favicon_ico():
    return redirect(url_for('static', filename='favicon.ico'))


class MarkdownFlaskUrlProcessor(markdown.util.Processor):

    def run(self, root):
        stack = [root]
        while stack:
            element = stack.pop()
            if element.tag == 'a':
                href = element.get('href')
                if href.startswith('flask:'):
                    element.set('href', url_for(href.split(':', 1)[1]))
            for child in element:
                stack.append(child)


def render_page(name):
    path = os.path.join('pages', name)
    with current_app.open_resource(path) as file:
        text = file.read().decode('utf8')
        md = Markdown(extensions=['meta'])
        md.treeprocessors["flask_links"] = MarkdownFlaskUrlProcessor(md)
        html = md.convert(text)
        title = ' '.join(md.Meta.get('title', []))
        return render_template('page.html', content=html, title=title)


def add_page_route(name, path=None):
    if path is None:
        path = '/' + name
    general_page.add_url_rule(path, name, lambda: render_page(name + '.md'))


add_page_route('index', '/')
add_page_route('chromaprint')
add_page_route('contact')
add_page_route('database')
add_page_route('docs')
add_page_route('donate')
add_page_route('faq')
add_page_route('fingerprinter')
add_page_route('license')
add_page_route('server')
add_page_route('webservice')
add_page_route('applications')
