#!/usr/bin/env python

from server import Server, render_template
from s3 import S3Backend

BUCKET_NAME = 'tinyhousebucket'

app = Server(__name__)
backend = S3Backend(BUCKET_NAME)


@app.route(r'^/$')
def index():
    return render_template('index.html', projects=backend.get_projects())


@app.route(r'^/([^/]*)/$')
def project(project_name):
    return render_template('project.html', project_name=project_name)


app.run('0.0.0.0', 8000)
