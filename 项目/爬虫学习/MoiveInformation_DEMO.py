# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 13:59:15 2017

@author: wind
"""

import requests
import re
from lxml import etree
from bs4 import BeautifulSoup


pageURL = u'https://movie.douban.com/subject/20514871/'
#随意选择一个电影页面
try:
    r = requests.get(pageURL)
except:
    print("页面读取失败")
html = etree.HTML(r.text)
bsObj = BeautifulSoup(r.text,'html.parser')
resultTitle =  html.xpath('//*[@id="content"]/h1/span[1]/text()')
#电影标题获取
resultLanguage = bsObj.find(text="语言:").parent.next_sibling
#电影语言获取
resultLanguage = re.sub('\s+','',resultLanguage)
#去掉空格
resultDate = bsObj.find(property="v:initialReleaseDate").get_text()
#电影上映日期获取
resultScore = bsObj.find(class_="ll rating_num").get_text()
#电影评分获取
resultScoreSampleNum = bsObj.find(property="v:votes").get_text()
print(resultTitle[0])
print(resultLanguage)
print(resultDate)
print(resultScore)
print(resultScoreSampleNum)
