from django.shortcuts import render

# Create your views here.
from authen.models import UserInfo

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from .models import LogColumn,LogPost,LogTag
from .forms import LogColumnForm,LogPostForm,LogTagForm
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger #内置分页模块
from statics.plugins.page.pager import Pagination #自定义分页
import json


#栏目增
@login_required(login_url='account/login/')
@csrf_exempt  #解决CSRF问题的另一种方式
def log_column(request):
    userinfo = UserInfo.objects.get(user=request.user)  # 用于header中的头像
    if request.method == "GET":

        columns=LogColumn.objects.filter(user=request.user)
        column_form=LogColumnForm()

        return render(request,'log/column/log_column.html',locals())
    if request.method == "POST":
        column_name=request.POST['column']
        # columns=LogColumn.objects.filter(user_id=request.user.id,column=column_name)#QuerySet 元素为LogColumn对象
        columns=LogColumn.objects.filter(user=request.user,column=column_name)#QuerySet 元素为LogColumn对象
        if columns:
            return HttpResponse("2")
        else:
            LogColumn.objects.create(user=request.user,column=column_name)
            return HttpResponse("1")

#栏目重命名
@login_required(login_url='account/login/')
@require_POST  #保证此函数只通过POST方式提交数据
@csrf_exempt
def rename_log_column(request):
    column_name=request.POST['column_name']
    column_id=request.POST['column_id']
    try:
        line=LogColumn.objects.get(id=column_id)
        line.column=column_name
        line.save()
        return HttpResponse("1")
    except:
        return HttpResponse("0")

#删除栏目
@login_required(login_url='account/login/')
@require_POST
@csrf_exempt
def del_log_column(request):
    column_id=request.POST['column_id']
    try:
        line=LogColumn.objects.get(id=column_id)
        line.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")

#编辑文章
@login_required(login_url='account/login/')
@csrf_exempt
def log_post(request):
    userinfo = UserInfo.objects.get(user=request.user)  # 用于header中的头像
    if request.method=="POST":
        log_post_form=LogPostForm(request.POST)

        if log_post_form.is_valid():
            cd=log_post_form.cleaned_data
            try:

                new_log=log_post_form.save(commit=False)
                new_log.author=request.user
                new_log.column=request.user.log_column.get(id=request.POST['column_id'])
                new_log.save()

                tags=request.POST['tags']
                if tags:
                    for atag in json.loads(tags):
                        tag=request.user.tag.get(tag=atag)
                        new_log.log_tag.add(tag)
                return HttpResponse("1")
            except Exception as e:
                print(e)
                return HttpResponse("2")
        else:
            return HttpResponse("3")
    else:
        log_post_form = LogPostForm()
        log_columns=request.user.log_column.all()
        log_tags=request.user.tag.all()
        return render(request,"log/column/log_post.html",locals())

#文章标题列表+自定义分页
@login_required(login_url='account/login/')
def log_list(request):
    userinfo = UserInfo.objects.get(user=request.user)  # 用于header中的头像
    log_list=LogPost.objects.filter(author=request.user)

    c_page=request.GET.get('page') #获取GET请求参数page的值

    page_obj = Pagination(len(log_list), c_page,"/log/log-list",perPageItemNum=5)
    logs = log_list[page_obj.start():page_obj.end()]

    return render(request,"log/column/log_list.html",locals())

#文章详情页
@login_required(login_url='account/login/')
def log_detail(request,id,slug):
    userinfo = UserInfo.objects.get(user=request.user)  # 用于header中的头像
    log=get_object_or_404(LogPost,id=id,slug=slug) #这句话是什么意思？？？
    return render(request,"log/column/log_detail.html",locals())

#删除文章
@login_required(login_url='account/login/')
@require_POST  #保证此函数只通过POST方式提交数据
@csrf_exempt
def del_log(request):
    log_id=request.POST['log_id']
    try:
        log=LogPost.objects.get(id=log_id)
        log.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")

#修改文章
@login_required(login_url='account/login/')
@csrf_exempt
def redit_log(request,log_id):
    userinfo = UserInfo.objects.get(user=request.user)  # 用于header中的头像
    if request.method=="GET":
        log_columns=request.user.log_column.all() #<QuerySet [<LogColumn:__str__ python>]>
        log=LogPost.objects.get(id=log_id)  #LogPost对象：__str__ 汇丰银行环境
        this_log_form=LogPostForm(initial={"title":log.title}) #初始化input标签

        this_log_column=log.column
        return render(request,"log/column/redit_log.html",locals())
    else:
        redit_log=LogPost.objects.get(id=log_id)
        try:
            redit_log.column=request.user.log_column.get(id=request.POST['column_id'])
            redit_log.title=request.POST['title']
            redit_log.body=request.POST['body']
            redit_log.save()
            return HttpResponse("1")
        except:
            return HttpResponse("2")

#管理标签
@login_required(login_url='account/login/')
@csrf_exempt
def log_tag(request):
    userinfo = UserInfo.objects.get(user=request.user)  # 用于header中的头像
    if request.method == "GET":
        log_tags=LogTag.objects.filter(author=request.user)
        log_tag_form=LogTagForm()
        return render(request,'log/tag/tag_list.html',locals())

    if request.method == "POST":
        tag_post_form=LogTagForm(data=request.POST)
        if tag_post_form.is_valid():
            try:
                new_tag=tag_post_form.save(commit=False)
                new_tag.author=request.user
                new_tag.save()
                return HttpResponse("1")
            except:
                return HttpResponse("the data cannot be save.")
        else:
            return HttpResponse("sorry,the form is not valid.")

#删除标签
@login_required(login_url='account/login/')
@require_POST
@csrf_exempt
def del_log_tag(request):
    tag_id=request.POST['tag_id']
    try:
        tag=LogTag.objects.get(id=tag_id)
        tag.delete()
        return HttpResponse('1')
    except:
        return HttpResponse('2')