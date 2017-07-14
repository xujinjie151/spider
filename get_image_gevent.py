# -*- coding: utf-8 -*-
# 使用grequests 重写，提高爬图速度

import os
import requests
import grequests
import time
from lxml import html
headers = {
        "headers" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36",
        "Referer" : "https://www.girl-atlas.com/?p=2",
    }

def get_response(url):
    try:
        response = requests.get(url, headers = headers)
        return response
    except Exception, e:
        raise e
    
    return None

# 获取每个页面的url
def get_page_urls():

    start_url = 'https://www.girl-atlas.com/'
    response = get_response(start_url)
    page_urls = []

    page_urls.append(start_url)
    while True:
        parsed_body = html.fromstring(response.text)
        next_url = parsed_body.xpath('//ul[@class="pagination"]/li[last()]/a/@href')
        print next_url

        if not next_url:
            break

        next_url = start_url + next_url[0]
        page_urls.append(next_url)
        response = get_response(next_url)

    print "get_page_urls done!!!"

    return page_urls

# 获取每个girl专辑的url
def get_girl_urls(page_urls):

    

    # 采用grequests，建立5个并发连接
    rs = (grequests.get(url, headers = headers) for url in page_urls)
    responses = grequests.map(rs, size = 5)
    
    for response in responses:
        if response:
            girl_urls = []
            parsed_body = html.fromstring(response.text)
            girl =  parsed_body.xpath('//div[@class="album-grid"]/a/@photo')
            girl_urls.extend(girl)

            get_images(girl_urls)
    
    # return girl_urls
    
# def get_image_urls(girl_urls):

#     girl_list = []

#     # 建立5个并发连接
#     rs = (grequests.get(url) for url in girl_urls)
#     responses = grequests.map(rs, size = 5)

#     for response in responses:
#         parsed_body = html.fromstring(response.text)
#         girl_title  = parsed_body.xpath('//title/text()')
#         image_urls = parsed_body.xpath('//li[@class="slide "]/img/@src | //li[@class="slide "]/img/@delay')

#         # print image_urls
#         girl_dict = {girl_title[0] : image_urls}
#         girl_list.append(girl_dict)
    
#     print "get_girl_urls done!!!"
#     return girl_list

def get_images(girl_list):


    # 图片的默认存储目录
    start_dir = 'D:/pic1'

    # https://girlatlas.b0.upaiyun.com/57653d9d58e039311fd01a15/20170407/0001_050849.jpg!mid
    # https://girlatlas.b0.upaiyun.com/57653d9d58e039311fd01a15/20170407/0001_050849.jpg!mid
    # https://girlatlas.b0.upaiyun.com/57653d9d58e039311fd01a15/20170407/0001_050849.jpg!mid

    rs = (grequests.get(url, headers = headers) for url in girl_list)
    responses = grequests.map(rs)

    image_dict = dict(zip(girl_list, responses))
    for url in image_dict:
        try:
            print url
        except Exception:
            pass 
        with open(start_dir + '/' + url.split('/')[-1][:-4], 'wb') as f:
            try:
                r = image_dict[url]
                f.write(r.content)
            except Exception:
                pass

   

if __name__ == '__main__':

    page_urls = get_page_urls()
    
    start_time = time.time()
    
    get_girl_urls(page_urls)
   
    # girl_list = get_image_urls(girl_urls)
    # print "girl %s" % len(girl_urls)
    # get_images(girl_urls)

    # elapsed_time = time.time() - start_time
    # print
    # print "elasped %s seconds!!!!" % elapsed_time
