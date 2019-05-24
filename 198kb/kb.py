#!/usr/bin/env python
#coding: utf-8

import cgi
import urllib2
import json
import httplib

form = cgi.FieldStorage()

raw_query = form["query"].value
query = raw_query
q_type = 0 #属性
if query.endswith('r'):
    q_type = 1
    query = query[:-1]

uniquery = query.decode("utf-8")
querylist = uniquery.split(u"的")

arg_len = len(querylist)
cql = 'START n0=node:node_auto_index(NAME="%s") ' % querylist[0]

if arg_len == 1:
    cql += "RETURN n0"
elif arg_len == 2:
    if q_type == 0:
        cql += "RETURN n0.`%s`" % querylist[1]
    else:
        cql += "MATCH (n0)-[:`%s`]->(b) RETURN b" % querylist[1]
else:
    i = 1
    while i < arg_len - 1:
        last_node = "n%d" % (i-1)
        cur_node = "n%d" % i
        cql += "MATCH (%s)-[:`%s`]->(%s) " % (last_node, querylist[i], cur_node)
        i += 1
    if q_type == 0:
        cql += "RETURN n%d.`%s`" % (i-1, querylist[arg_len-1])
    else:
        cql += "MATCH (n%d)-[:`%s`]->(n%d) RETURN n%d" % (i-1, querylist[arg_len-1], i, i)

query_dict = {
        'query' : cql,
        'params' : {}
        }
query_str = json.dumps(query_dict, ensure_ascii=False).encode("utf-8")
#print "Content-Type: application/json; charset=UTF-8\r"
#print "\r"
#print query_str
#exit()

request_head = {
        'Accept' : "application/json; charset=UTF-8",
        'Content-Type' : "application/json"
        }
conn = httplib.HTTPConnection("localhost:7474")
conn.request('POST',"/db/data/cypher",query_str,headers=request_head)
res = conn.getresponse().read()
conn.close()

pageStr = '''
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
</head>
<body>
<form action="/cgi-bin/graph_demo.py" method="get">
    查询: <input type="text" name="query" style = "width:400" value="%s"/>
	<input type="submit" value="submit"/>
</form>
<hr />
<xmp>
%s
</xmp>
</body>
</html>
'''

print "Content-Type: text/html; charset=UTF-8\r"
print "\r"
#print pageStr % (raw_query, res)
print res
