# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 14:08:40 2018

@author: wind
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','untitled1.settings')
import django
django.setup()
from MoiveRe.models import Rating,Movie,MovielensUser
import datetime
import pytz

def save(uid,mid,rating,time):
    try:
        flag = Rating.objects.get_or_create(
        user=MovielensUser.objects.get(id=uid),
        movie=Movie.objects.get(id=mid),
        rating=rating,
        datetime=time,
        )
    except BaseException:
        with open('rating_log.txt', 'a+') as log:
            log.writelines(uid+' '+mid+' '+rating+' '+time+'\n')
    finally:

        print(flag[1])


path = 'E:\\python learning\\'
local_tz = pytz.timezone('Asia/Shanghai')
with open(path+'u.data','r') as f:
    i = 0
    for line in f:
        uid,mid,rating,time=line.split()
        uid = int(uid)
        mid = int(mid)
        rating = int(rating)
        time = datetime.datetime.fromtimestamp(int(time))
        time = local_tz.localize(time)
        save(uid, mid, rating, time)
        i = i + 1
        print(i)