#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django import template

register=template.Library()

from moment.models import LogPost
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

#文章总数
@register.simple_tag
def total_logs():
    return LogPost.objects.count()

#作者文章数
@register.simple_tag
def author_total_logs(user):
    return user.log.count()

#最新发表的文章
@register.inclusion_tag('log/list/latest_logs.html')
def latest_logs(n=5):
    latest_logs=LogPost.objects.order_by("-created")[:n]
    return locals()

#最多评论文章
@register.simple_tag
def most_commented_logs(n=3):
    return LogPost.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:n]

@register.filter(name='markdown') #将函数markdown_filter名字修改为markdown
def markdown_filter(text):
    return mark_safe(markdown.markdown(text))

