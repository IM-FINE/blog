#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django import forms
from slugify import slugify
from .models import Image

class ImageForm(forms.ModelForm):
    class Meta:
        model=Image
        fields=('title','description','image')
