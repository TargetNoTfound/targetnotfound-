

# Create your views here.
from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from .form import RegisterForm , RatingForm
from MoiveRe.models import MovielensUser, Movie, MovieRatingTimes, Rating, MovieRatingAvg, MovieRecommend
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import pandas as pd
from surprise import SVD
from surprise import Dataset
from surprise import Reader
import datetime

def home(request):
    if cache.get('df') is not None:
        pass
    else:
        data = Rating.objects.values_list('movie_id', 'user_id', 'rating').all()

        ratingdict = {
            'item_id': [],
            'user_id': [],
            'rating': [],
        }

        for rating in data:
            ratingdict['item_id'].append(rating[0])
            ratingdict['user_id'].append(rating[1])
            ratingdict['rating'].append(rating[2])

        df = pd.DataFrame(ratingdict)
        print(df)
        cache.set('df', df)
    return render(request, 'index.html')


def register(request):
    # 只有当请求为 POST 时，才表示用户提交了注册信息
    if request.method == 'POST':
        # request.POST 是一个类字典数据结构，记录了用户提交的注册信息
        # 这里提交的就是用户名（username）、密码（password）、邮箱（email）
        # 用这些数据实例化一个用户注册表单
        form = RegisterForm(request.POST)
        # 验证数据的合法性
        if form.is_valid():
            # 如果提交数据合法，调用表单的 save 方法将用户数据保存到数据库
            user = form.save()
            movieuser = MovielensUser(user=user)
            movieuser.save()
            login(request, user)
            # 注册成功，跳转回首页
            return redirect('/movie')
    else:
        # 请求不是 POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
        form = RegisterForm(request.POST)
    # 渲染模板
    # 如果用户正在访问注册页面，则渲染的是一个空的注册表单
    # 如果用户通过表单提交注册信息，但是数据验证不合法，则渲染的是一个带有错误信息的表单
    return render(request, 'register.html', context={'form': form})


@login_required(login_url='/movie/login')
def quickre(request):
    print(cache.get('df'))
    return render(request, 'quickre.html',)


def quick_rating(requst):
    page = int(requst.GET['page'])
    uid = int(requst.GET['uid'])
    user = MovielensUser.objects.get(user_id=uid)
    uid = user.id
    re_movie = Rating.objects.values('movie_id').filter(user_id=uid)
    re_movie = list(re_movie)
    re_movie_id = []
    for movie in re_movie:
        re_movie_id.append(int(movie['movie_id']))
    movies = MovieRatingTimes.objects.values('movie_id').order_by('-rating_times')
    movies = list(movies)
    movies_id = []
    for movie in movies:
        movies_id.append(int(movie['movie_id']))



    for movie in re_movie_id:
        if movie in movies_id:

            movies_id.remove(movie)

    for i in range(page):
         for j in range(8):
             movies_id.pop(0)
    movies_id = movies_id[:8]
    movies = []
    for id in movies_id:
        movies.append(Movie.objects.get(id=id))

    return render(requst,'moive_load.html',{'movies':movies})

def rating(requst):
    user = requst.user
    user = MovielensUser.objects.get(user_id=user.id)
    rating = requst.POST

    mid = int(rating['mid'])

    rating = int(rating['rating'])

    record = Rating.objects.filter(user_id=user.id).filter(movie__id=mid)

    df = cache.get('df')
    cache.delete('df')
    if record:
        Rating.objects.filter(user_id=user.id).filter(movie__id=mid).update(rating=rating)
        df = df[(df.item_id != mid) | (df.user_id != user.id)]
        df = df.append({
            'item_id': mid,
            'user_id': user.id,
            'rating': rating,
        }, ignore_index=True)
        cache.set('df', df)
    else:
        flag = Rating.objects.get_or_create(
            user=MovielensUser.objects.get(id=user.id),
            movie=Movie.objects.get(id=mid),
            rating=rating,
            datetime=datetime.datetime.now(),
        )
        df = df.append({
            'item_id': mid,
            'user_id': user.id,
            'rating': rating,
        }, ignore_index=True)
        cache.set('df', df)
    print(df)
    return HttpResponse(True)

def quick_predict(request):
    user = request.user
    user = MovielensUser.objects.get(user_id=user.id)
    moive_watched = Rating.objects.values_list('movie_id').filter(user_id=user.id)
    if not moive_watched:
        return render(request, 'quick_predict.html', context={
            'movies': None,
            'warning':'您尚未为任何一部电影评分，请在评分后使用快速推荐功能'
        })
    moive_watched = list(moive_watched)
    temp = []
    for movie in moive_watched:
        temp.append(movie[0])
    moive_watched = temp
    df = cache.get('df')
    read = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(df[['user_id', 'item_id', 'rating']], read)
    trainset = data.build_full_trainset()
    algo = SVD()
    algo.fit(trainset)

    number = 1683
    predciton = []
    for i in range(1, number + 1):
        if i not in moive_watched:
            pred = algo.predict(944, i)
            predciton.append([i, pred.est])
    predciton = sorted(predciton, key=lambda i: i[1], reverse=True)[:8]
    moive_id = []
    for movie in predciton:
        moive_id.append(movie[0])
    movies = Movie.objects.filter(id__in=moive_id)
    print(movies)
    return render(request, 'quick_predict.html', context={
        'movies': movies,
    })


@login_required(login_url='/movie/login')
def detail(requst,pk):
    user = requst.user
    user = MovielensUser.objects.get(user_id=user.id)
    rating = Rating.objects.filter(user_id=user.id, movie_id=pk)
    if rating:
        rating = rating[0]
    moive = get_object_or_404(Movie, pk=pk)
    moive_avg_rating = get_object_or_404(MovieRatingAvg, pk=pk)
    return render(requst, 'detail.html', context={'movie': moive,
                                                  'avg_rating': moive_avg_rating,
                                                  'rating':rating})




@login_required(login_url='/movie/login')
def mylist(requst):
    user = requst.user
    user = MovielensUser.objects.get(user_id=user.id)
    movies = Rating.objects.filter(user=user).order_by('datetime')
    paginator = Paginator(movies, 8)
    page = requst.GET.get('page')
    try:
        movie_list = paginator.page(page)
    except PageNotAnInteger:
        movie_list = paginator.page(1)
    except EmptyPage:
        movie_list = paginator.page(paginator.num_pages)

    return render(requst, 'mylist.html', context={
                                         'movies':movie_list,
                                        'page': movie_list,
                                        'paginator': paginator,
                                        })

@login_required()
def recommend(requst):
    user = requst.user
    user = MovielensUser.objects.get(user_id=user.id)
    movies = MovieRecommend.objects.filter(user=user).order_by('-rating_est')
    paginator = Paginator(movies, 8)
    page = requst.GET.get('page')
    try:
        movie_list = paginator.page(page)
    except PageNotAnInteger:
        movie_list = paginator.page(1)
    except EmptyPage:
        movie_list = paginator.page(paginator.num_pages)

    return render(requst, 'recommend.html', context={
        'movies': movie_list,
        'page': movie_list,
        'paginator': paginator,
    })
