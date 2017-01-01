from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$',views.first_page,name='first_page'),
    url(r'^staff/',views.staff,name='staff'),
    url(r'^templay',views.templay,name='templay'),
    url(r'^form/',views.form,name='form'),
    url(r'^investigate',views.investigate,name='investigate')
]
