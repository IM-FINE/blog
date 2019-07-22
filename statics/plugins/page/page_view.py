#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.shortcuts import render
from statics.plugins.page.pager import Pagination

#自定义分页
USER_LIST = []
for i in range(1,666):
    temp = {'name':'root'+str(i), 'age':i}
    USER_LIST.append(temp)
def index2(request):
    current_page = request.GET.get('p')
    page_obj = Pagination(666,current_page)

    data_list = USER_LIST[page_obj.start():page_obj.end()]
    return render(request,'index2.html',{'data':data_list,'page_obj':page_obj})