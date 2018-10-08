from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class MovielensUser(models.Model):
    user = models.OneToOneField(User, related_name='lid', on_delete=models.CASCADE, null=True)


class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(max_length=100)
    imgurl = models.TextField(max_length=200)
    summary = models.TextField(max_length=200)

    def get_absolute_url(self):
        return reverse('moive:detail' ,kwargs={'pk': self.id})


class Rating(models.Model):
    user = models.ForeignKey(MovielensUser, related_name='luser', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='lmovie', on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    datetime = models.DateTimeField()
    class Meta:
        unique_together=("user","movie")

class MovieRecommend(models.Model):
    user = models.ForeignKey(MovielensUser, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating_est = models.DecimalField(max_digits=14, decimal_places=4)
    add_time = models.DateTimeField(auto_created=True)

class MovieRatingAvg(models.Model):
    movie_id = models.IntegerField(primary_key=True)
    avg_rating = models.DecimalField(max_digits=14, decimal_places=4, blank=True, null=True)

    def __str__(self):
        return '%.2f'%self.avg_rating

    class Meta:
        managed = False
        db_table = 'movie_rating_avg'


class MovieRatingTimes(models.Model):
    movie_id = models.IntegerField()
    rating_times = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'movie_rating_times'

