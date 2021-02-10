from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout,authenticate,login
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from main.models import ListTweet
# Create your views here.
def register(request):
    if request.method == "POST":
        reg_form = UserRegisterForm(request.POST)
        if reg_form.is_valid():
            reg_form.save()
            username = reg_form.cleaned_data.get('username')
            return redirect('index')
    else:
        reg_form = UserRegisterForm()
    context={
        'form':reg_form
    }
    return render(request, 'register.html',context=context)
def my_login(request):
    return render(request, 'login.html')
def my_logins(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username,password=password)
    if user is not None:
        login(request,user)
        return redirect('/')
    else:
        return redirect('login')
def my_logout(request):
    logout(request)
    return redirect('index')
@login_required
def managementroom(request):
    list = ListTweet.objects.all()
    context={
        'list':list
    }
    return render(request, 'management.html',context=context)
def deletetweet(request,tweet_id):
    tweet = ListTweet.objects.get(pk=tweet_id)
    tweet.delete()
    return redirect('main_manage')