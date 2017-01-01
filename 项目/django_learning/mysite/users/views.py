#coding=utf8
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.contrib.auth import *
from django.http import HttpResponse

def user_login(request):
    '''
    login
    '''
    if request.POST:
        username = password = ''
        username = request.POST.get('username')
        password = request.POST.get('password')
        user     = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return diff_response(request)
        else:
            return diff_response(request)
    ctx = {}    
    ctx.update(csrf(request))
    return render(request, 'login.html',ctx)

def user_logout(request):
    '''
    logout
    URL:/users/logout
    '''
    logout(request)
    return redirect('/')

def diff_response(request):
    if request.user.is_authenticated():
        content = "<p>my dear user</p>"
    else:
        content = "<p>you wired stranger</p>"
    return HttpResponse(content)

from django.contrib.auth.forms import UserCreationForm
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
        return redirect("/")
    else:
        form = UserCreationForm()
        ctx = {'form':form}
        ctx.update(csrf(request))
        return render(request,"register.html",ctx)

def login_test(request):
    return render(request,'login_test.html')
