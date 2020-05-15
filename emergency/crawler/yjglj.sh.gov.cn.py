import os.path
import json
import base64
import gzip
import requests
import pyce3
import urllib.parse
from requests_html import HTMLSession

url = 'http://yjglj.sh.gov.cn/info/iList.jsp?node_id=GKxxgk&tm_id=41&cat_id=10111&gk_index=&topic_key=&title=%E6%8A%A5%E5%91%8A'

def content(url):
    print(f"\t{url}")
    f = url[url.rfind('/')+1:]
    fname = f"yjglj.sh.gov.cn/{f}"
    if os.path.isfile(fname):
        content = open(fname,"rb").read()
    else:
        r = requests.get(url)
        content = r.content
        with open(fname, "wb") as out:
            out.write(content)
    ret = {}
    if url.endswith("html") or url.endswith("htm"):
        enc, ret['time'], title, ret['text'], _ = pyce3.parse(url, content)
        ret['from'] = 'html'
    ret['gzip_content'] = base64.b64encode(gzip.compress(content)).decode('utf-8')
    return ret

out = open("yjglj.sh.gov.cn.json", "w")
session = HTMLSession()
while True:
    print(url)
    r = session.get(url)
    nodes = r.html.xpath('//div[@class="info-list"]//tbody/tr')
    for node in nodes:
        item = {
            'url': list(node.absolute_links)[0],
            "title": node.find("a")[0].attrs['title'],
            "seq": node.xpath(".//td[2]")[0].text,
            "date": node.xpath(".//td[3]")[0].text,
        }
        ret = content(item['url'])
        item.update(ret)
        out.write(json.dumps(item, ensure_ascii=False)+"\n")
    link = r.html.find("a:contains('下一页')")
    if len(link) <= 0 or len(nodes) < 15:
        break
    url = list(link[0].absolute_links)[0]
    url = url.replace("/info/", "/info/iList.jsp")
session.close()
out.close()
