# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 18:08:50 2018

@author: wind
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','untitled1.settings')
import django
django.setup()
import csv
import requests
from lxml import etree
from MoiveRe.models import Movie

def save(mID,title,img,summary):
    movie = Movie.objects.get_or_create(id=int(mID), name=title, imgurl=img, summary=summary)
    print(movie[1])

def crawl(mID, iID):
    base_url = 'https://www.imdb.com/title/tt'
    try:
        r = requests.get(base_url + iID)
        html = etree.HTML(r.text)
        title = html.xpath('//h1[@itemprop="name"]/text()')[0]
        year = html.xpath('//span[@id="titleYear"]/a/text()')[0]
        title = title + '(' + year + ')'
        img = html.xpath('//div[@class=\'poster\']//img/@src')[0]
        summary = html.xpath('//div[@class="summary_text"]/text()')[0]
        summary = summary.rstrip().lstrip()
        save(mID, title, img, summary)
    except BaseException :
        print(mID+'出错')
        with open('log.txt', 'a+') as id:
            id.writelines(mID+'\n')

max = 1682  # ml-100k

with open('E:\python learning\links.csv', newline='') as imdbID:
    reader = csv.DictReader(imdbID)

    for row in reader:
        print(row['movieId'])
        try:
            if int(row['movieId']) > 27:
                crawl(row['movieId'], row['imdbId'])
            else:
                continue
        finally:
            if int(row['movieId']) > max:
                break

