#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.conf.urls import url
from . import views


urlpatterns=[
    url(r'^manage-images/$',views.manage_images,name='manage_images'),
    url(r'^upload-image/$',views.upload_image,name='upload_image'),
    url(r'^edit-image/$',views.edit_image,name='edit_image'),
    url(r'^del-image/$',views.del_image,name='del_image'),
    url(r'^images/$',views.falls_images,name='falls_images'),
]