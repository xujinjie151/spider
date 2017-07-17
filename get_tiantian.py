# -*- coding: utf-8 -*-
import requests
HEADERS = {"User-Agent":r"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"}
from lxml import html
import grequests
page_urls = []
for l in range(1,20):
    page_urls.append("http://guba.eastmoney.com/list,of110011_"+str(l)+".html")
    
rs = (grequests.get(url, headers = HEADERS) for url in page_urls)
responses = grequests.map(rs, size = 5)

for response in responses:
    if response:
        girl_urls = []
        parsed_body_1 = html.fromstring(response.text)
        # 讨论内容
#         fundComment1 = parsed_body_1.xpath('//div[@class="articlelistnew"]//text()')
        # 讨论内容
        fundComment1 = parsed_body_1.xpath('//div[@class="articleh"]//text()')
#         去空
        for x in fundComment1:
            if x.strip() == "":
                fundComment1.remove(x)
#  分段
        for y in range(len(fundComment1)):
            if len(fundComment1[y].strip()) == 0:
                fundComment1[y] = "@@@"

        print ("\n".join(" ".join(fundComment1).split("@@@")))