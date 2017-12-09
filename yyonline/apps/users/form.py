# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 15:12:47 2017

@author: Administrator
"""
from django import forms
from captcha.fields import CaptchaField

from  .models import UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(required=True) #要求html中名称一致
    password = forms.CharField(required=True,min_length=5)

class RegisterForm(forms.Form):
    is_teacher = forms.BooleanField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        #form name
        fields = ['image']

class ModifyPwdForm(forms.Form):
    # 密码一直
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        #form name
        fields = ['nick_name','gender','birday','address','mobile']