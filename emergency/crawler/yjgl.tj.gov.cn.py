import io
import os.path
import json
import base64
import gzip
import requests
from requests_html import HTMLSession
import pyce3

def main():
    url = 'http://yjgl.tj.gov.cn/tj/zhengwugongkai/shiguzhuanlan/diaochabaogao/index.html'
    session = HTMLSession()
    out = open("yjgl.tj.gov.cn.json", "w")
    print(url)
    r = session.get(url)
    for node in r.html.find("li.page_t"):
        item = {
            "url": list(node.absolute_links)[0],
            "title": node.find("a")[0].attrs['title'],
            "date": node.find("span.fr")[0].text,
        }
        ret = content(item['url'])
        item.update(ret)
        print(item)
        out.write(json.dumps(item, ensure_ascii=False)+"\n")
    session.close()
    out.close()

def content(url):
    print(f"\t{url}")
    f = url[url.rfind('/')+1:]
    fname = f"yjgl.tj.gov.cn/{f}"
    if os.path.isfile(fname):
        content = open(fname,"rb").read()
    else:
        r = requests.get(url)
        content = r.content
        with open(fname, "wb") as out:
            out.write(content)
    ret = {}
    if url.endswith("html"):
        enc, ret['time'], title, ret['text'], _ = pyce3.parse(url, content)
        ret['from'] = 'html'
    ret['gzip_content'] = base64.b64encode(gzip.compress(content)).decode('utf-8')
    return ret


if __name__ == "__main__":
    main()
