import random
import redis
import json
import redis

def get_link(handler):
    r = redis.Redis(host='localhost', port=6379, db=0)
    link = r.get('link')
    if link is not None:
        link = json.loads(link.decode('utf-8'))
        print(link)
        handler.set_response(200, link['url'])
        r.delete('link')
    else:
        handler.set_response(204, '')