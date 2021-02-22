import requests
from bs4 import BeautifulSoup
import json
import time
import threading
from fake_useragent import UserAgent

searches = [
    {
        'item': '3080',
        'url': 'https://www.newegg.com/p/pl?d=3080&N=100007709&isdeptsrh=1&LeftPriceRange=690+925'
    },
    {
        'item': '3070',
        'url': 'https://www.newegg.com/p/pl?d=3070&N=100007709&isdeptsrh=1&LeftPriceRange=490+700'
    },
    {
        'item': '3060ti',
        'url': 'https://www.newegg.com/p/pl?d=3060ti&N=100007709&isdeptsrh=1&LeftPriceRange=390+560'
    },
    {
        'item': '5700XT',
        'url': 'https://www.newegg.com/p/pl?d=5700xt&N=100007709&isdeptsrh=1&LeftPriceRange=390+560'
    },
    {
        'item': '5600XT',
        'url': 'https://www.newegg.com/p/pl?d=5600xt&N=100007709&isdeptsrh=1&LeftPriceRange=260+400'
    }
]

def main():
    threads = []
    for search in searches:
        t = threading.Thread(target=search_loop, args=(search,))
        t.start()
        time.sleep(1)
        threads.append(t)

def search_loop(search):
    while True:
        try:
            (result, link_count) = check_url(search['url'])
            if result is not None:
                print(str(time.time()) + ":", search['item'], "IN STOCK (" + str(link_count) + ") items")
                link = {
                    'url': result,
                    'item': search['item'],
                    'message': "New Egg " + search['item'] + " is in stock",
                    'volume': 6
                }
                report_link(link)
            else:
                print(str(time.time()) + ":", search['item'], "out of stock (" + str(link_count) + ") items")
        except Exception as e:
            print(e)
        time.sleep(7)

def check_url(url):
    ua = UserAgent()
    headers = {
        'Host': 'www.newegg.com',
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    links = soup.select('.item-cells-wrap .item-cell')
    for link in links:
        if 'OUT OF STOCK' not in str(link) and "txt-ads-link" not in str(link):
            item_link = link.select("a.item-title")[0]
            return (item_link['href'], len(links))
    return (None, len(links))

def report_link(link):
    requests.post('http://10.8.0.30:19546/alert', json.dumps(link))

if __name__ == '__main__':
    main()
