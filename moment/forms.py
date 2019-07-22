#!/usr/bin/env python
#-*- coding:utf-8 -*-
from django import forms
from .models import LogColumn,LogPost,Comment,LogTag

class LogColumnForm(forms.ModelForm):
    class Meta:
        model=LogColumn
        fields=("column",)

class LogPostForm(forms.ModelForm):
    class Meta:
        model=LogPost
        fields=("title","body",)

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=("body",)

class LogTagForm(forms.ModelForm):
    class Meta:
        model=LogTag
        fields=('tag',)