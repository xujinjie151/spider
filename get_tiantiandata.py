# coding: utf-8


import requests
HEADERS = {"User-Agent":r"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"}
from lxml import html
import grequests



response = requests.get("http://fund.eastmoney.com/api/Dtshph.ashx?t=0&c=yndt&s=desc&issale=&page=1&psize=2400",headers = HEADERS)

parsed_body_1 = html.fromstring(response.text)



import pandas as pd
pp1 = pd.DataFrame([], columns =  ["fund_id", "fund_num","fund_name","fund_onevalue","fund_time","fund_1year","fund_2year","fund_3year","fund_5year","fund_star","fund_fee"])

fund_id = parsed_body_1.xpath('//tr//td[2]//text()')
pp1.fund_id = fund_id
fund_num = parsed_body_1.xpath('//tr//td[3]//text()')
pp1.fund_num = fund_num
fund_name = parsed_body_1.xpath('//tr//td[4]//text()')
pp1.fund_name = fund_name
fund_onevalue = parsed_body_1.xpath('//tr//td[6]//text()')
pp1.fund_onevalue= fund_onevalue
fund_time = parsed_body_1.xpath('//tr//td[7]//text()')
pp1.fund_time = fund_time
fund_1year = parsed_body_1.xpath('//tr//td[8]//text()')
pp1.fund_1year = fund_1year
fund_2year = parsed_body_1.xpath('//tr//td[9]//text()')
pp1.fund_2year = fund_2year
fund_3year = parsed_body_1.xpath('//tr//td[10]//text()')
pp1.fund_3year = fund_3year
fund_5year = parsed_body_1.xpath('//tr//td[11]//text()')
pp1.fund_5year = fund_5year
fund_star = parsed_body_1.xpath('//tr//td[12]//text()')
def y5(x):
    if "暂无评级" in x:
        return 0
    else:
        return len(x)
fund_star = [y5(x) for x in fund_star]
pp1.fund_star = fund_star
fund_fee = parsed_body_1.xpath('//tr//td[13]//text()')
pp1.fund_fee = fund_fee



import os
os.chdir(os.path.abspath('D:\\PycharmProjects\\spider'))

# 保存排名数据
pp1.to_csv("jijin1.csv")


# 基金代码
list_num = pp1["fund_num"].values


pp2 = pd.DataFrame([], columns =  ["id", "comment","time"])
def getComment(code):
    page_urls = []
    for l in range(1,2):
        page_urls.append("http://guba.eastmoney.com/list,of"+code+"_"+str(l)+".html")

    rs = (grequests.get(url, headers = HEADERS) for url in page_urls)
    responses = grequests.map(rs, size = 5)

    for response in responses:
        if response:
            girl_urls = []
            parsed_body_1 = html.fromstring(response.text)
            # 讨论内容
            fundComment1 = parsed_body_1.xpath('//div[@class="articleh"]//text()')


            quit_list = ["讨论","话题","公告","置顶"]
            for x in quit_list:
                while x in fundComment1:
                    ii = fundComment1.index(x)
                    fundComment1[ii+2] = "MYMARK " + fundComment1[ii+2]
                    fundComment1.remove(x)
            
            #             去空
            for x in fundComment1:
                if x.strip() == "":
                    fundComment1.remove(x)
            
            #             去空
            for x in fundComment1:
                if x.strip() == "":
                    fundComment1.remove(x)
            try:
                for c in range(len(fundComment1)):
                    if c % 6 == 2:
                        fundComment1[c] = fundComment1[c] +" TIMESPLIT "+ fundComment1[c+3]
                        
                for j in [(fundComment1[b]) for b in range(len(fundComment1)) if b % 6 == 2 and not fundComment1[b][:6] == "MYMARK"] :
                    pp2.loc[len(pp2)] = [code,j.split("TIMESPLIT")[0],j.split("TIMESPLIT")[1]]
            except Exception as e:
                print(e)
                print(code)
                
    

# 获取评论数据
import time
for z in list_num[0:100]:
    print(z)
    getComment(z)
    time.sleep(0.2)



import os
os.chdir(os.path.abspath('D:\\PycharmProjects\\spider'))

pp2.to_csv("comment1.csv")


import re

# 获取历史价值
def hisvalue(code):
    os.chdir(os.path.abspath('D:\\PycharmProjects\\spider\\data'))
    pp3 = pd.DataFrame([], columns =  ["id", "time","value","hisvalue","dayrate"])
    page_urls = []
    for l in range(1,100):
        page_urls.append("http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code="+code+"&page="+str(l))

    rs = (grequests.get(url, headers = HEADERS) for url in page_urls)
    responses = grequests.map(rs, size = 5)

    for response in responses:
        fundRang = re.search("content:\"(.*?)\"", response.text, re.S).group(1)
        parsed_body = html.fromstring(fundRang)
        for k in range(1,11):
            fundName = parsed_body.xpath('//table//tbody//tr[' + str(k) + ']//text()')
            if len(fundName) >3:
                pp3.loc[len(pp3)] = {"id":len(pp3), "time":fundName[0] , "value":fundName[1] , "hisvalue":fundName[2] , "dayrate":fundName[3]}

    pp3.to_csv(code+".csv")



for y in list_num[0:100]:
    hisvalue(y)



for y in list_num[:20]:
    getComment(y)


