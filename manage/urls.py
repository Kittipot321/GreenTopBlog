"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from main import urls
from manage import urls,views
urlpatterns = [
   path('', views.managementroom, name='main_manage'),
   path('addpost/', views.addtweet, name='add'),
   path('editpost/<int:tweet_id>', views.edittweet, name='edit'),
   path('editpost/<int:tweet_id>/setstatus', views.editstatus, name='editstatus'),
   path('deletepost/<int:tweet_id>', views.deletetweet, name='delete'),
   path('deletecomment/<int:comment_id>', views.deletecomment, name='delete_cm'),
]
