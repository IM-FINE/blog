from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from slugify import slugify

class LogColumn(models.Model):

    user=models.ForeignKey(User,related_name="log_column",on_delete=models.CASCADE)
    column=models.CharField(max_length=200)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.column


# 标签
class LogTag(models.Model):
    author = models.ForeignKey(User, related_name='tag', on_delete=models.CASCADE)
    tag = models.CharField(max_length=500)

    def __str__(self):
        return self.tag

class LogPost(models.Model):

    author=models.ForeignKey(User,related_name="log",on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    slug=models.SlugField(max_length=500)
    column=models.ForeignKey(LogColumn,related_name="log_post",on_delete=models.CASCADE)
    body=models.TextField()
    created=models.DateTimeField(default=timezone.now())
    update=models.DateTimeField(auto_now=True)

    log_tag=models.ManyToManyField(LogTag,related_name='log_tag',blank=True)

    users_like=models.ManyToManyField(User,related_name="log_like",blank=True) #多对多

    class Meta:
        ordering=("title",)
        index_together=(('id','slug'),)

    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        self.slug=slugify(self.title)
        super(LogPost,self).save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse("log:log_detail",args=[self.id,self.slug])

    def get_url_path(self):
        return reverse("log:read_log",args=[self.id,self.slug])

#评论
class Comment(models.Model):
    log=models.ForeignKey(LogPost,related_name="comments",on_delete=models.CASCADE)
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=('-created',)
