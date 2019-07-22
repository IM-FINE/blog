#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.conf.urls import url
from django.contrib.auth.views import LoginView,LogoutView
from .views import ListUserInfoView,RegisterView,EditUserInfoView

urlpatterns = [
    # 内置登录类
    url(r"^login/$", LoginView.as_view(template_name='authen/login.html'), name="user_login"),
    url(r"^logout/$",LogoutView.as_view(template_name='authen/logout.html'),name="user_logout"),
    url(r"^user-info/$",ListUserInfoView.as_view(),name="user_info"),
    url(r"^register/$",RegisterView.as_view(),name="user_register"),
    url(r"^edit-info/$",EditUserInfoView.as_view(),name="edit_info"),
]
