from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
# Create your models here.
class ListTweet(models.Model):
    title = models.CharField(max_length=255,null=False)
    content = RichTextField(blank=True,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    status = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now=False, null=True)
    updated_date = models.DateTimeField(auto_now=True,null=False)
    def total_comment(self):
        return self.comment_set.count()
    def __str__(self):
        return self.title
class Comment(models.Model):
    content = models.TextField(max_length=255)
    create_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(ListTweet, on_delete=models.CASCADE, null=True)
