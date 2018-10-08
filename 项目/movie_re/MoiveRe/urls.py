from django.urls import path, include

from . import views
app_name = 'moive'
urlpatterns = [
    path(r'register/', views.register, name='register'),
    path(r'', views.home, name='home'),
    path(r'quickre', views.quickre, name='quick'),
    path(r'quickrating', views.quick_rating, name='quick_rating'),
    path(r'rating', views.rating, name='rating'),
    path(r'detail/<int:pk>/', views.detail, name='detail'),
    path(r'quick_predict/', views.quick_predict, name='quick_predict'),
    path(r'search/', include('haystack.urls'), name='search'),
    path(r'mylist/', views.mylist, name='mylist'),
    path(r'recommend', views.recommend, name='recomment'),
]