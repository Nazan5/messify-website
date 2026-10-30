"""Tell Bing (and other IndexNow search engines, which feed ChatGPT search and Copilot) about every page in the sitemap.

Run after a change has gone live:  python3 indexnow.py
"""
import json, re, urllib.request

KEY = '06934ffe8fbc10dabc365b3a90dc08e3'
HOST = 'www.messify.me'

urls = re.findall(r'<loc>([^<]+)</loc>', open('dist/sitemap.xml').read())
body = json.dumps({'host': HOST, 'key': KEY, 'keyLocation': f'https://{HOST}/{KEY}.txt', 'urlList': urls}).encode()
req = urllib.request.Request('https://api.indexnow.org/indexnow', data=body,
                             headers={'Content-Type': 'application/json; charset=utf-8'})
with urllib.request.urlopen(req, timeout=30) as r:
    print('IndexNow:', r.status, f'({len(urls)} URLs submitted)')
