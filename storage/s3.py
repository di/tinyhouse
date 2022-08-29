from urllib import request
import xml.etree.ElementTree as ET


class S3Backend:

    def __init__(self, bucket_name):
        self.ns = {
            's3': 'http://s3.amazonaws.com/doc/2006-03-01/'
        }
        self.bucket_name = bucket_name

    def get_projects(self):
        resp = request.urlopen(
            'http://{}.s3.amazonaws.com?delimiter=/'.format(self.bucket_name)
        ).read()

        root = ET.fromstring(resp)

        return [
            prefix.text.rstrip('/')
            for prefix in root.find('s3:CommonPrefixes', self.ns)
        ]

    def get_files_for_project(self):
        pass
