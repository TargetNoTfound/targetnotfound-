import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','untitled1.settings')
import django
django.setup()
from MoiveRe.models import Rating, MovielensUser, MovieRecommend, Movie
from surprise import SVD
from surprise import Dataset
from surprise import Reader
import datetime
import pandas as pd

data = Rating.objects.values_list('movie_id','user_id','rating').all()
movies_watched = Rating.objects.values_list('movie_id').filter(user_id=944)

movies_id = []
for mo in movies_watched:
    movies_id.append(mo[0])

ratingdict = {
    'item_id':[],
    'user_id':[],
    'rating':[],
}

for rating in data:
    ratingdict['item_id'].append(rating[0])
    ratingdict['user_id'].append(rating[1])
    ratingdict['rating'].append(rating[2])

df = pd.DataFrame(ratingdict)
print(df)
read = Reader(rating_scale=(1,5))

data = Dataset.load_from_df(df[['user_id', 'item_id', 'rating']], read)
trainset = data.build_full_trainset()
algo = SVD()
algo.fit(trainset)

number = 1683
predciton = []
for i in range(1,number+1):
    if i in movies_id:
        continue
    pred = algo.predict(944, i,verbose=True )
    predciton.append([i,pred.est])
predciton = sorted(predciton, key = lambda i : i[1] ,reverse=True)[:40]
print(predciton)

for re in predciton:
    MovieRecommend.objects.create(movie_id=re[0],user_id=944,rating_est=re[1],add_time=datetime.datetime.now())
