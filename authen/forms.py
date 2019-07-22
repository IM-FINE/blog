#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from .models import UserInfo

from slugify import slugify

class RegistrationForm(forms.ModelForm):
    '''注册表单'''

    password=forms.CharField(label="Password",widget=forms.PasswordInput)
    password2=forms.CharField(label="Confirm Password",widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=("username","email")

    def clean_password2(self):
        cd=self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("passwords do not match.")
        return cd['password2']


class UserInfoForm(forms.ModelForm):
    '''用户信息表单'''

    class Meta:
        model=UserInfo
        fields=("birth","phone","school","company","profession","address","aboutme","portrait")

class UserForm(forms.ModelForm):
    '''用户表单，邮箱'''

    class Meta:
        model=User
        fields=("email",)

