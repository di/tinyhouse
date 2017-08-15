#!/usr/bin/env python
import string
import re
from http.server import HTTPServer, BaseHTTPRequestHandler


class App():

    def __init__(self, name):
        self.name = name
        self.routes = {}

    def route(self, path):
        def decorator(function):
            self.routes[path] = function
        return decorator

    def run(self, host='127.0.0.1', port=5000):
        routes = self.routes

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                for route, route_function in routes.items():
                    match = re.match(route, self.path)
                    if match:
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write(
                            route_function(*match.groups()).encode()
                        )
                        break
                else:
                    self.send_response(404)

        print('Running...')
        httpd = HTTPServer((host, port), Handler)
        httpd.serve_forever()


app = App(__name__)

projects = [
    'frob', 'spamspamspam', 'blahblahblahblah3'
]


class Formatter(string.Formatter):

    def format_field(self, value, spec):
        if spec.startswith('repeat'):
            template = spec.partition(':')[-1]
            if type(value) is dict:
                value = value.items()
            return ''.join([template.format(item=item) for item in value])
        else:
            return super(Formatter, self).format_field(value, spec)


def render_template(template_name, **context):
    formatter = Formatter()
    with open('./templates/' + template_name) as template:
        template_string = template.read()
    return formatter.format(template_string, **context)


@app.route(r'^/$')
def index():
    return render_template('index.html', projects=projects)


@app.route(r'^/([^/]*)/$')
def project(project_name):
    return render_template('project.html', project_name=project_name)


app.run('0.0.0.0', 8000)
