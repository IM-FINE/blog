from django.db import models

# Create your models here.

from django.contrib.auth.models import User  # django自带的认证模块


class UserInfo(models.Model):
    '''用户信息表，与User表为一对一关系'''

    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    birth = models.DateTimeField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    school = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    profession = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    aboutme = models.TextField(blank=True)  # 对应HTML中的Textarea
    portrait = models.ImageField(blank=True, upload_to='images/portr'
                                                       'ait/p_%Y_%m_%d')  # 头像，可以为空

    def __str__(self):
        return 'user:{}'.format(self.user.username)
