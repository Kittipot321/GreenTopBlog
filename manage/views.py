from tokenize import Comment
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout,authenticate,login
from django.contrib.auth.decorators import login_required
from .forms import EditTweetForm, UserRegisterForm,AddTweetForm
from datetime import datetime
from main.models import ListTweet,Comment
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
    # Management Comment Page if blogger is see all comments but end-user is see you comment.
    list = ListTweet.objects.all().order_by('-id')
    if request.user.is_superuser:
        list = list
    else:
        list = ListTweet.objects.filter(user=request.user)
    search_txt = request.GET.get('search','')
    if search_txt:
        list = list.filter(title__contains=search_txt)
    for onelist in list:
        # Counting the number of comments on each post and then saving it to the number_of_comment attribute of the post.
        onelist.number_of_comment = onelist.comment_set.filter(post=onelist.id).count()
    context={
        'list':list
    }
    return render(request, 'management.html',context=context)

@login_required
def addtweet(request):
    # Saving the form with the instance of the tweet.
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

@login_required
def edittweet(request,tweet_id):
    # Getting the tweet with the primary key of tweet_id, and then it is saving the form with the
    # instance of the tweet.
    instance = ListTweet.objects.get(pk=tweet_id)
    form = EditTweetForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('main_manage')
    context={
        'form':form,
        'edit_id':tweet_id
    }
    return render(request, 'editpage.html',context=context)

@login_required
def deletetweet(request,tweet_id):
    """
    It deletes the tweet with the id of tweet_id and then redirects to the main_manage page
    
    :param request: The request object is the first parameter to every view function. It contains
    information about the request that was made to the server
    :param tweet_id: The id of the tweet you want to delete
    :return: the redirect function.
    """
    tweet = ListTweet.objects.get(pk=tweet_id)
    tweet.delete()
    return redirect('main_manage')

@login_required
def deletecomment(request,comment_id):
    """
    It gets the comment with the primary key of comment_id, deletes it, and then redirects to the page
    of the post that the comment was on
    
    :param request: The request object is a standard Django object that contains metadata about the
    request sent to the server
    :param comment_id: The id of the comment to be deleted
    :return: The comment is being deleted and the user is being redirected to the page of the post that
    the comment was on.
    """
    comment = Comment.objects.get(pk=comment_id)
    comment.delete()
    return redirect('each_a_page',news_id=comment.post.id)

@login_required
def editstatus(request, tweet_id):
    post = ListTweet.objects.get(pk=tweet_id)
    if post.status == True:
        post.status = False
    else:
        post.status = True
    post.save()
    return redirect('main_manage')