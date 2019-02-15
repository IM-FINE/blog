#!/usr/bin/env python
#-*- coding:utf-8 -*-
from django.shortcuts import render,HttpResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger #内置分页模块
from .models import LogColumn,LogPost,Comment
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Count
from authen.models import UserInfo

import redis
from django.conf import settings
#连接redis
r=redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=settings.REDIS_DB)


from statics.plugins.page.pager import Pagination

#自定义分页
def log_titles(request,username=None):
    if request.user.is_authenticated:
        userinfo = UserInfo.objects.get(user=request.user)  # 用于header中的头像
    if username:
        user=User.objects.get(username=username)
        log_title=LogPost.objects.filter(author=user)
        try:  #用户可能没有填写自己的信息
            userinfo=user.userinfo
        except:
            userinfo=None
    else:
        log_title=LogPost.objects.all()

    c_page = request.GET.get('page')
    page_obj = Pagination(len(log_title), c_page,"/log/list-log-titles",perPageItemNum=3)
    logs = log_title[page_obj.start():page_obj.end()]

    if username:
        return render(request,"log/list/author_logs.html",locals())
    else:
        return render(request,"log/list/log_titles.html",locals())

#文章详情页
#不检查用户是否登录
def read_log(request,id,slug):
    userinfo = UserInfo.objects.get(user=request.user)  # 用于header中的头像
    log=get_object_or_404(LogPost,id=id,slug=slug) #这句话是什么意思？？？
    total_views=r.incr("log:{}:views".format(log.id))#incur函数，让当前的键值递增并返回递增后的值
    r.zincrby('log_ranking',1,log.id) #文章被访问一次，log_ranking将文章的id的值增加1

    log_ranking=r.zrange('log_ranking',0,-1,desc=True)[:10]
    log_ranking_ids=[int(id) for id in log_ranking]
    most_viewed=list(LogPost.objects.filter(id__in=log_ranking_ids))
    most_viewed.sort(key=lambda x:log_ranking_ids.index(x.id))

    if request.method == "POST":
        comment_form=CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment=comment_form.save(commit=False)
            new_comment.log=log
            new_comment.save()
        else:
            comment_form=CommentForm()

    log_tags_ids=log.log_tag.values_list("id",flat=True) #flat=True返回列表，只返回id，不加返回元组并返回id和对应的对象
    #exclude排除当前文章
    similar_logs=LogPost.objects.filter(log_tag__in=log_tags_ids).exclude(id=log.id)
    similar_logs=similar_logs.annotate(same_tags=Count("log_tag")).order_by('-same_tags','-created')[:4]
    return render(request,"log/list/read_log.html",locals())

#点赞
@login_required(login_url='account/login/')
@require_POST  #保证此函数只通过POST方式提交数据
@csrf_exempt
def like_log(request):
    log_id=request.POST.get("id")
    action=request.POST.get("action")
    if log_id and action:
        try:
            log=LogPost.objects.get(id=log_id)
            if action=='like':
                log.users_like.add(request.user)
                return HttpResponse('1')
            else:
                log.users_like.remove(request.user)
                return HttpResponse('2')
        except:
            return HttpResponse('no')

