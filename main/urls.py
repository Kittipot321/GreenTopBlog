# Create your tests here.
from main import views
from django.urls import path
from django.contrib import admin
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('news/<int:news_id>', views.each_a_page, name='each_a_page'),
    path('addtweet/', views.addtweet, name='addpage'),
]