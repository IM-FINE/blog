from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from slugify import slugify

class Image(models.Model):
    user=models.ForeignKey(User,related_name='images',on_delete=models.CASCADE)
    title=models.CharField(max_length=300)
    slug=models.SlugField(max_length=500,blank=True)
    description=models.TextField(blank=True)
    created=models.DateField(auto_now_add=True,db_index=True)
    image=models.ImageField(upload_to='images/image/im_%Y_%m_%d') #ImageField数据库中为varchar，主要是给admin用

    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        self.slug=slugify(self.title)
        super(Image,self).save(*args,**kwargs)