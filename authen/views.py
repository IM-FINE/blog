from django.shortcuts import render, HttpResponse, render, redirect, get_object_or_404,HttpResponseRedirect

# Create your views here.

from django.views.generic import View
from braces.views import LoginRequiredMixin
from django.contrib.auth import authenticate, login  # django内置认证
from .models import UserInfo
from django.contrib.auth.models import User
from .forms import UserInfoForm,RegistrationForm,UserForm
import os
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.urls import reverse #跳转到指定页面

class HomeView(View):
    '''主页'''

    def get(self, request):
        if request.user.is_authenticated:
            userinfo = UserInfo.objects.get(user=request.user)
            return render(request,'home.html',locals())
        else:
            return render(request,'home.html',locals())

class UserInfoMixin(LoginRequiredMixin):
    '''用户未登录跳转'''
    model = UserInfo
    login_url = 'account/login/'

@method_decorator(csrf_exempt,name='dispatch')
class ListUserInfoView(UserInfoMixin,View):
    '''列出个人信息及上传头像'''

    def get(self, request):

        user = User.objects.get(username=request.user.username)
        userinfo = UserInfo.objects.get(user=user)

        info_list = [
            {"用户名：": user.username},
            {"邮箱：": user.email},
            {"生日：": userinfo.birth.date()},
            {"电话：": userinfo.phone},
            {"毕业院校：": userinfo.school},
            {"工作单位：": userinfo.company},
            {"职业：": userinfo.profession},
            {"地址：": userinfo.address},
            {"个人介绍：": userinfo.aboutme},
        ]
        return render(request,'authen/userinfo.html',locals())

    def post(self, request):

        valid_extensions = ['jpg', 'jpeg', 'png']
        try:
            portrait = request.FILES['portrait']
            portrait_type = str(portrait).rsplit('.', 1)[1].lower()
            if portrait_type in valid_extensions:
                if len(portrait) > 1048576:
                    return HttpResponse("1")
                else:
                    userinfo = UserInfo.objects.get(user=request.user.id)
                    if userinfo.portrait:
                        userinfo.portrait.delete()
                        del_path = os.path.join(settings.MEDIA_ROOT, str(userinfo.portrait))
                        os.remove(del_path)
                    userinfo.portrait = portrait
                    userinfo.save()
                    return HttpResponse("2")
            else:
                return HttpResponse("3")
        except Exception as e:
            print(e)
            return HttpResponse("4")

class RegisterView(View):
    '''注册'''

    def get(self,request):
        form=RegistrationForm()
        info=UserInfoForm()
        return render(request,"authen/register.html",locals())

    def post(self,request):
        form=RegistrationForm(request.POST)
        info=UserInfoForm(request.POST)
        if form.is_valid() * info.is_valid():
            new_user=form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()

            new_info=info.save(commit=False)
            new_info.user=new_user
            new_info.save()

            UserInfo.objects.create(user=new_user)

            return HttpResponseRedirect(reverse("account:user_login"))
        else:
            return HttpResponse("sorry,register failed")




@method_decorator(csrf_exempt,name='dispatch')
class EditUserInfoView(UserInfoMixin,View):
    '''编辑个人信息'''

    def get(self,request):
        user = User.objects.get(username=request.user.username)
        userinfo = UserInfo.objects.get(user=request.user)
        # initial初始化input标签
        user_form = UserForm(instance=request.user)
        userinfo_form = UserInfoForm(initial={"birth": userinfo.birth,
                                              "phone": userinfo.phone,
                                              "school": userinfo.school,
                                              "company": userinfo.company,
                                              "profession": userinfo.profession,
                                              "address": userinfo.address,
                                              "aboutme": userinfo.aboutme
                                              })

        info_list = [{"用户名：": user.username},
                     {"邮箱：": user_form['email']},
                     {"生日：": userinfo_form['birth']},
                     {"电话：": userinfo_form['phone']},
                     {"毕业院校：": userinfo_form['school']},
                     {"工作单位：": userinfo_form['company']},
                     {"职业：": userinfo_form['profession']},
                     {"地址：": userinfo_form['address']},
                     {"个人介绍：": userinfo_form['aboutme']},
                     ]

        return render(request, 'authen/edit_info.html', locals())

    def post(self,request):
        user = User.objects.get(username=request.user.username)
        userinfo = UserInfo.objects.get(user=request.user)
        user_form=UserForm(request.POST)
        userinfo_form=UserInfoForm(request.POST)
        if user_form.is_valid() *  userinfo_form.is_valid():
            user_cd=user_form.cleaned_data
            userinfo_cd=userinfo_form.cleaned_data

            user.email=user_cd['email']
            userinfo.birth=userinfo_cd['birth']
            userinfo.phone=userinfo_cd['phone']
            userinfo.school=userinfo_cd['school']
            userinfo.company=userinfo_cd['company']
            userinfo.profession=userinfo_cd['profession']
            userinfo.address=userinfo_cd['address']
            userinfo.aboutme=userinfo_cd['aboutme']

            user.save()
            userinfo.save()

            return HttpResponseRedirect('/authen/user-info/')


