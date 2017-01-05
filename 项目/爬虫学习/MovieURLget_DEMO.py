# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 09:56:52 2017

@author: wind
"""

from lxml import etree
import requests
import re

URL = u'https://movie.douban.com/tag/惊悚' #从标签页获取电影的URL
payload = {'start':'0','type':'T'} #页面参数 start:起始项目数 
parrten = '\s+|\/' #删去标题中多余的空格和/
page = 5 #爬取的页面总数
MovieURLset = {}
for i in range(page):
    payload['start'] = str(i*20) #一页20个项目
    try:
        r = requests.get(URL,params=payload)
        #豆瓣电影 惊悚 标签
    except:
        print("页面读取错误")
    html = etree.HTML(r.text)
    resultTitle = html.xpath('//*[@class="article"]/div[2]/table/tr/td[2]'
                        '/div/a')  #title
    resultURL = html.xpath('//*[@class="article"]/div[2]/table/tr/td[2]'
                        '/div/a/@href')   #链接
    #Chrome的xpath分析为’//*[@id="content"]/div/div[1]/div[2]/
    #                  table[1]/tbody/tr/td[2]/div/a‘
    #实际上tbody标签是由浏览器加上去的 源html并没有这一项
    for (MoveTitle,MovieURL) in zip(resultTitle,resultURL):
        MovieURLset[re.sub(parrten,'', MoveTitle.text)]=MovieURL
        #删去title中的无效字符
for keys,values in MovieURLset.items():
    print(keys+" : "+values)