#!/usr/bin/env python

from server import Server, render_template


app = Server(__name__)

projects = [
    'frob', 'spamspamspam', 'blahblahblahblah3'
]


@app.route(r'^/$')
def index():
    return render_template('index.html', projects=projects)


@app.route(r'^/([^/]*)/$')
def project(project_name):
    return render_template('project.html', project_name=project_name)


app.run('0.0.0.0', 8000)
