from src.helpers import get_value
import os
import webbrowser
import threading
import time
import subprocess
import redis
import json

def get_alert(handler):
    with open('src/alert.html', 'r') as f:
        handler.set_response(200, f.read(), 'text/html')

def post_alert(handler):
    r = redis.Redis(host='localhost', port=6379, db=0)
    data = handler.get_json_post_data()

    item = get_value(data, 'item')
    message = get_value(data, 'message')
    vol = get_value(data, 'volume')
    url = get_value(data, 'url')

    link_data = {
        'item': item,
        'url': url
    }

    tasks = []
    key = 'item-' + item
    existing_item = r.get(key)
    if existing_item is None:
        r.set(key, '', ex=120)
        r.set('link', json.dumps(link_data).encode('utf-8'))

        if message is not None:
            x = threading.Thread(target=play_alert, args=(message,vol,), daemon=True)
            x.start()
            tasks.append(x)
        if url is not None:
            x = threading.Thread(target=open_browser, args=(url,), daemon=True)
            x.start()
            tasks.append(x)

    for task in tasks:
        task.join()

    handler.set_response(200, '')

def play_alert(message, volume):
    if volume is None:
        volume = 5

    os.system(f'osascript -e "set Volume {volume}"')
    subprocess.Popen(['say', message])

def open_browser(url):
    webbrowser.open_new(url)
