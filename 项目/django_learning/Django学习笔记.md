#Django 学习笔记
**基本参考<https://www.shiyanlou.com/courses/214>**

仅对基于个人环境出现的配置与代码差异进行记录
##环境
	wind@wind-VirtualBox:~/mysite/west$ python --version
	Python 2.7.12
	wind@wind-VirtualBox:~/mysite/west$ python -m django --version
	1.10.4
	wind@wind-VirtualBox:~/mysite/west$ mysql --version
	mysql  Ver 14.14 Distrib 5.7.16, for Linux (x86_64) using  EditLine wrapper
	
##局域网访问网页
`$python manage.py runserver 0.0.0.0:8000`

同时需要配置`ALLOWED_HOSTS`(`setting.py`)
	
	ALLOWED_HOSTS = [
		u'192.168.0.50', 
		u'192.168.0.100'     
	#	'*',  #该项启用则允许所有地址访问                                                  
	]   
参考自<https://segmentfault.com/a/1190000003756582>

##第一个网页
在“第一个网页”这一章中mysite/mysite/url.py中的代码按照django 1.10格式范例才能正常运行自定义中文首页。

	from django.conf.urls import url
	from django.contrib import admin
	from . import views

	urlpatterns = [
		url(r'^admin/', admin.site.urls),
		url(r'^$', views.first_page, name='first_page'),
	]

##增加APP页面
`west/urls.py`

	from django.conf.urls import url
	from . import views
	urlpatterns = [
		url(r'^$',views.first_page,name='first_page'),
		url(r'^staff/',views.staff,name='staff'),
	]
##连接数据库
###mysql设置

	GRANT SELECT, INSERT, UPDATE, REFERENCES,DELETE, CREATE, DROP, INDEX, ALTER, CREATE TEMPORARY TABLES, LOCK TABLES ON wind_dj.* TO 'wind'@'localhost' IDENTIFIED BY 'lishuang4';

###Django设置
`setting.py`

	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.mysql',
			'NAME': 'wind_dj',
			'USER': 'wind',
			'PASSWORD': 'lishuang4',
			'HOST': 'localhost',
			'PORT':'3306',
    		}
	}
###POST方法
`from django.core.context_processors import csrf`

应变更为

`from django.template.context_processors import csrf`

###用户登录
`login.html`

    1 <form role="form"  action='/users/' method="post">          
    2      {% csrf_token %}                                          
    3     <label>Username</label>                         
    4     <input type="text" name='username'>                      
    5     <label>Password</label>                                                            
    6     <input name="password" type="password">                                       
    7     <input type="submit" value="Submit">                                         
    8 </form>        
