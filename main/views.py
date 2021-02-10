from django.shortcuts import render,redirect
from django.http import HttpResponse
from main.models import ListTweet,Comment
from django.contrib.auth.decorators import login_required
from manage.forms import AddTweetForm,CommentForm
from datetime import datetime
# Create your views here.
def index(request):
    mydb = ListTweet.objects.all().order_by('-id')
    search_txt = request.GET.get('search','')
    if search_txt:
        mydb = mydb.filter(title__contains=search_txt)
    context={
        'db':mydb
    }
    return render(request, "index.html",context=context)

def each_a_page(request,news_id):
    mydb = ListTweet.objects.filter(pk=news_id)
    comment = Comment.objects.filter(post_id=news_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            instance = form.save()
            instance.user_id = request.user.id
            instance.post_id = news_id
            instance.save()
            return redirect('each_a_page', news_id=news_id)
    else:
        form = CommentForm()
    context={
        'db':mydb,
        'form':form,
        'comment':comment
    }
    return render(request, "each_a_page.html", context=context)
@login_required
def addtweet(request):
    if request.method == "POST":
        form = AddTweetForm(request.POST)
        if form.is_valid():
            instance = form.save()
            instance.user_id = request.user.id
            instance.create_date = datetime.now()
            instance.save()
            return redirect('index')
    else:
        form = AddTweetForm()
    context={
        'form':form
    }
    return render(request, 'addpage.html',context=context)