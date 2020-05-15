import io
import os.path
import json
import base64
import gzip
import requests
from requests_html import HTMLSession
import pyce3
import pdfplumber

def main():
    url = 'https://www.mem.gov.cn/gk/sgcc/tbzdsgdcbg/index.shtml'
    u = 'https://www.mem.gov.cn/gk/sgcc/tbzdsgdcbg/index_%d.shtml'
    session = HTMLSession()
    out = open("www.mem.gov.cn.json", "w")
    while True:
        print(url)
        r = session.get(url)
        for node in r.html.xpath("//table//table//a"):
            title, date = node.text[:-10], node.text[-10:]
            item = {
                'url':list(node.absolute_links)[0],
                'title':title, "date":date,
            }
            try:
                ret = content(item['url'])
                item.update(ret)
            except Exception as e:
                print(e)
            out.write(json.dumps(item, ensure_ascii=False)+"\n")
        curr = int(r.html.search('var currentPage = {};//')[0])
        total = int(r.html.search('var countPage = {}//')[0])
        page = curr + 1
        if page >= total: break
        url = u % page
    session.close()
    out.close()

def content(url):
    print(f"\t{url}")
    f = url[url.rfind('/')+1:]
    fname = f"www.mem.gov.cn/{f}"
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
    elif url.endswith(".pdf"):
        pdf = pdfplumber.load(io.BytesIO(content))
        ret['text'] = ''.join([page.extract_text() for page in pdf.pages])
        ret['from'] = 'pdf'
    ret['gzip_content'] = base64.b64encode(gzip.compress(content)).decode('utf-8')
    return ret


if __name__ == "__main__":
    main()
