import io
import os.path
import json
import base64
import gzip
import urllib.parse
from requests_html import HTMLSession
import requests
import pyce3
import pdfplumber
import subprocess
import docx

headers = {
'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
'Accept-Encoding': 'gzip, deflate', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
}

def content(url):
    print(f"\t{url}")
    f = url[url.rfind('/')+1:]
    fname = f"yjglj.beijing.gov.cn/{f}"
    if os.path.isfile(fname):
        content = open(fname,"rb").read()
    else:
        r = requests.get(url, headers=headers)
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
    elif url.endswith(".doc"):
        ret['text'] = subprocess.check_output(["antiword", fname]).decode('utf-8')
        ret['from'] = 'doc'
    elif url.endswith(".docx"):
        word = docx.Document(fname)
        ret['text'] = '\n'.join([x.text for x in word.paragraphs])
        ret['from'] = 'docx'
    ret['gzip_content'] = base64.b64encode(gzip.compress(content)).decode('utf-8')
    return ret


url = 'http://yjglj.beijing.gov.cn/col/col4520/index.html'
session = HTMLSession()
print(url)
r = session.get(url)
iurls = r.html.search_all("urls[i] = '{}';")
whos = r.html.search_all('headers[i] = "{}";')
titles = r.html.search_all("year[i] = '{}';")
urls = r.html.search_all("xkrq[i] ='{}';")
session.close()

out = open("yjglj.beijing.gov.cn.json", "w") 
for i, iurl in enumerate(iurls):
    iurl = urllib.parse.urljoin(url, iurl[0])
    xurl = urllib.parse.urljoin(url, urls[i][0])
    who = whos[i][0]
    title = titles[i][0]
    item = {'url':xurl, 'iurl':iurl, 'who':who, 'title': title}
    try:
        ret = content(item['url'])
        item.update(ret)
    except Exception as e:
        print(e)
    out.write(json.dumps(item, ensure_ascii=False)+"\n")
out.close()
