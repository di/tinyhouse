#!/usr/bin/env python
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


@app.route(r'^/$')
def index():
    project_link_template = '<a href="/{project_name}/">{project_name}</a><br/>'
    project_links = '\n'.join(
        project_link_template.format(project_name=project_name)
        for project_name in projects
    )
    return '''
<html>
  <body>
    {project_links}
  </body>
</html>
'''.format(project_links=project_links)


@app.route(r'^/([^/]*)/$')
def project(project_name):
    return '''
<html>
  <head>
    <title>Links for {project_name}</title>
  </head>
  <body>
    <h1>Links for {project_name}</h1>
    <a href="https://files.pythonhosted.org/packages/24/71/30c44bcfed678298cc0054fad03d2fb9dd5cb0635aaeb4085eb15c28f17c/blahblahblahblah3-13.13.13.tar.gz#sha256=673763d1cb12caffb29d50f24c2480457e1917a79168e371a3ada7b1403304b5">blahblahblahblah3-13.13.13.tar.gz</a><br>
  </body>
</html>
'''.format(project_name=project_name)


app.run('0.0.0.0', 8000)
