from http.server import BaseHTTPRequestHandler, HTTPServer
from cgi import parse_header, parse_multipart, parse_qs
from urllib.parse import parse_qsl, urlparse
import src.handlers as handlers
from src.helpers import parse_json
import json
import threading
import multiprocessing
import os

def MakeRequestHandler():
    class RequestHandler(BaseHTTPRequestHandler):
        def __init__(self, request, client_address, server):
            super(BaseHTTPRequestHandler, self).__init__(request, client_address, server)

        def do_GET(self):
            path = urlparse(self.path).path
            if path == '/alert':
                handlers.get_alert(self)
            elif path == '/link':
                handlers.get_link(self)
            else:
                self.set_response(404, '404', 'text/plain')

        def do_POST(self):
            path = urlparse(self.path).path
            if path == '/alert':
                handlers.post_alert(self)
            else:
                self.set_response(404, '404', 'text/plain')

        def do_DELETE(self):
            path = urlparse(self.path).path
            self.set_response(404, '404', 'text/plain')

        def set_response_raw(self, status_code, content, content_type = 'application/json', extra_headers = {}):
            self.send_response(status_code)
            self.send_header('Content-Type', content_type)
            for key, value in extra_headers.items():
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(content)

        def set_response(self, status_code, content, content_type = 'application/json', extra_headers = {}):
            self.set_response_raw(status_code, content.encode('utf-8'), content_type, extra_headers)

        def get_raw_post_data(self):
            length = int(self.headers['content-length'])
            return self.rfile.read(length)

        def get_form_post_data(self):
            ctype, pdict = parse_header(self.headers.get('content-type'))
            if ctype == 'multipart/form-data':
                return parse_multipart(self.rfile, pdict)
            elif ctype == 'application/x-www-form-urlencoded':
                length = int(self.headers.get('content-length'))
                return parse_qs(self.rfile.read(length), keep_blank_values=1)
            else:
                print('oh no')
                return dict()

        def get_json_post_data(self):
            data = self.get_raw_post_data()
            return parse_json(data, None)

        def parse_url_query(self):
            query = urlparse(self.path).query
            return dict(parse_qsl(query))

    return RequestHandler
