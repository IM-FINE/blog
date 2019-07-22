#!/usr/bin/env python
#-*- coding:utf-8 -*-
from django.conf.urls import url
from . import views,list_views

urlpatterns=[
    url(r"^log-column/$",views.log_column,name="log_column"),
    url(r"^rename-column/$",views.rename_log_column,name="rename_log_column"),
    url(r"^del-column/$",views.del_log_column,name="del_log_column"),
    url(r"^log-post/$",views.log_post,name="log_post"),
    url(r"^log-list/$",views.log_list,name="log_list"),
    url(r"^log-detail/(?P<id>\d+)/(?P<slug>[-\w]+)/$",views.log_detail,name="log_detail"),
    url(r"^del-log/$",views.del_log,name="del_log"),
    url(r"^redit-log/(?P<log_id>\d+)/$",views.redit_log,name="redit_log"),

    url(r"^list-log-titles/$",list_views.log_titles,name="log_titles"),
    url(r"^list-log-titles/(?P<username>[-\w]+)/$",list_views.log_titles,name="author_logs"),

    #在同一URL配置文件中不要出现相同的name
    url(r"^list-log-detail/(?P<id>\d+)/(?P<slug>[-\w]+)/$",list_views.read_log,name="read_log"),

    url(r"^like-log/$",list_views.like_log,name="like_log"),

    url(r"^log-tag/$",views.log_tag,name="log_tag"),
    url(r"^del_log-tag/$",views.del_log_tag,name="del_log_tag"),
]