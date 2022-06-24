from django.shortcuts import render,redirect
from main.models import ListTweet,Comment
from manage.forms import CommentForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Create your views here.
def index(request):
    mydb = ListTweet.objects.filter(status=True).order_by('-id')
    paginator = Paginator(mydb, 4)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    search_txt = request.GET.get('search','')
    if search_txt:
        post_list = mydb.filter(title__contains=search_txt)
    context={
        'db':post_list,
        'title':"GreenBlog"
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
        'comment':comment,
        'title':mydb[0].title
    }
    return render(request, "each_a_page.html", context=context)