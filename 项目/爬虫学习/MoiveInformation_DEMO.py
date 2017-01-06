# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 13:59:15 2017

@author: wind
"""

import requests
import re
from lxml import etree
from bs4 import BeautifulSoup
import pymysql.cursors

with open("date.txt","r") as f:
    connection = pymysql.connect(host='localhost',
                                 user='wind',
                                 password='lishuang4',
                                 db='spiderdata',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
    
    for pageURL in f:
        pageURL = re.sub("\s+","",pageURL) #删去末尾的换行符
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
        resultID = re.search('\d+',pageURL)
        resultID = resultID.group(0)
        print(resultTitle[0])
        print(resultLanguage)
        print(resultDate)
        print(resultScore)
        print(resultScoreSampleNum)
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `douban_movies` (`ID`, `Title`,`Language`,`Score`,`ScoreSampleNum`,`Date`)VALUES (%s, %s, %s,%s,%s,%s)"
                cursor.execute(sql, (resultID,resultTitle[0],resultLanguage
                                     ,resultScore,resultScoreSampleNum, resultDate))
            connection.commit()
        except:
            pass
    connection.close()