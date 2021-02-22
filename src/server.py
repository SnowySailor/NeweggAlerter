from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from src.request_handler import MakeRequestHandler
import redis

def run_server():
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.flushdb()
    server = HTTPServer(('', 19546), MakeRequestHandler())
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    print('Started server. Listening at http://localhost:19546')
