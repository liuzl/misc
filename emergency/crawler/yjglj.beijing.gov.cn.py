import json
import urllib.parse
from requests_html import HTMLSession
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
    out.write(json.dumps(item, ensure_ascii=False)+"\n")
out.close()
