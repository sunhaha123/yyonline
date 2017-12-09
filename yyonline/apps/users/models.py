# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models

# Create your models here.
from django.contrib.auth.models import  AbstractUser
from  organization.models import CourseOrg

class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50,verbose_name=u'昵称')
    birday = models.DateField(null=True,blank=True,verbose_name=u'生日',default='2010-01-01')
    gender = models.CharField(max_length=6,choices=(("male",u"男"),("female",u"女")),default=u"女",verbose_name=u'性别')
    address = models.CharField(max_length=100,default=u'',verbose_name=u'地址')
    mobile = models.CharField(max_length=11,null=True,blank=True,verbose_name=u'手机号')
    image = models.ImageField(upload_to="image/%Y/%m",default=u'image/default.png',max_length=100,verbose_name=u'头像')
    # birthday = models.DateField(null=True, blank=True, verbose_name=u'生日', default='2010-01-01')
    # is_staff = models.BooleanField(default=False,verbose_name=u'是否为教练')

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u"验证码")
    email = models.EmailField(max_length=50, verbose_name=u"邮箱地址")
    send_type = models.CharField(choices=(("register",u"注册"),("forget",u"找回密码")),max_length=10, verbose_name=u"验证码类型")
    send_time = models.DateField(default=datetime.now, verbose_name=u"发送时间")

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural  = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code,self.email)

class Banner(models.Model):
    title =  models.CharField(max_length=100, verbose_name=u"标题")
    image = models.ImageField(upload_to="banner/%Y/%m",max_length=100,verbose_name="轮播图片")
    url = models.URLField(max_length=200,verbose_name="访问地址")
    index = models.IntegerField(default=100,verbose_name=u"顺序")
    add_time = models.TimeField(default=datetime.now,verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name

