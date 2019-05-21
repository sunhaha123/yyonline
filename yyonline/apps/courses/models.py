# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from organization.models import CourseOrg,Teacher
from  users.models import  UserProfile


# Create your models here.

class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name=u"模型名称", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u"课程名")
    is_banner = models.BooleanField(default=False, verbose_name=u"是否轮播")
    teacher = models.ForeignKey(Teacher, verbose_name=u"讲师", null=True, blank=True)
    desc = models.CharField(max_length=300, verbose_name=u"课程描述")
    detail = models.TextField(verbose_name=u"课程详情")
    degree = models.CharField(max_length=30, choices=(("cj", "初级"), ("zj", "中级"), ("gj", "高级")), verbose_name=u"难度")
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长(分钟数)")
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    image = models.ImageField(max_length=100, upload_to='courses/%Y%m', verbose_name=u"封面图")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    category = models.CharField(default="后端开发", max_length=20, verbose_name=u"课程分类")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    youneed_know = models.CharField(max_length=500, verbose_name=u"课程须知", default="")
    teacher_tell = models.CharField(max_length=500, verbose_name=u"老师告知", default="")
    tag = models.CharField(default='',verbose_name="课程标签",max_length=10)

    class Meta:
        verbose_name = u"识别模型"
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        #反向获取课程章节数
        return  self.lesson_set.all().count()

    def get_learn_users(self):
        #反向获取课程用户信息
        return self.usercourse_set.all()[:3]

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course,verbose_name=u"课程")
    name = models.CharField(max_length=100,verbose_name=u"章节名")
    add_time = models.DateTimeField(verbose_name=u"添加时间")

    class Meta:
        verbose_name=  u"课程章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



class Video(models.Model):
    lesson = models.ForeignKey(Lesson,verbose_name=u"章节")
    name = models.CharField(max_length=100,verbose_name=u"视频名")
    add_time = models.DateTimeField(verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class CourseResource(models.Model):
    course = models.ForeignKey(Course,verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"课程名")
    add_time = models.DateTimeField(verbose_name=u"添加时间")
    download = models.FileField(upload_to="course/resource/%Y/%m",verbose_name=u"资源信息",max_length=100)

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u"标题")
    image = models.ImageField(max_length=100, upload_to="banner/%Y%m", verbose_name=u"轮播图")
    url = models.URLField(max_length=200, verbose_name=u"访问地址")
    index = models.IntegerField(default=100, verbose_name=u"顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name

class Sensor(models.Model):
    image = models.ImageField(max_length=100, upload_to="sensor/%Y%m", verbose_name=u"曲线图", default="")
    category = models.CharField(max_length=100, verbose_name=u"运动类别",default="1")
    user = models.ForeignKey(UserProfile, verbose_name=u"用户", null=True, blank=True)

    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name


class activityID(models.Model):
    # image = models.ImageField(max_length=100, upload_to="sensor/%Y%m", verbose_name=u"曲线图", default="")
    name = models.CharField(max_length=20, verbose_name=u"运动类别",)
    # user = models.ForeignKey(UserProfile, verbose_name=u"用户", null=True, blank=True)

    class Meta:
        verbose_name = u"运动种类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class SportData(models.Model):
    action_time = models.DateTimeField(default=datetime.now, verbose_name=u"创建时间")
    user = models.ForeignKey(UserProfile, verbose_name=u"用户", null=True, blank=True)
    sportid = models.ForeignKey(activityID,verbose_name=u"运动类别")
    rate = models.IntegerField(verbose_name=u"心率",blank=True,null=True)
    position = models.IntegerField(verbose_name=u"传感器位置", default=0)
    type = models.IntegerField(verbose_name=u"传感器种类 ", default=0)
    data_x = models.FloatField(verbose_name=u"传感器x轴数据")
    data_y = models.FloatField(verbose_name=u"传感器y轴数据")
    data_z = models.FloatField(verbose_name=u"传感器z轴数据")

    class Meta:
        verbose_name = u"运动数据"
        verbose_name_plural = verbose_name

    # def __str__(self):
    #     return self.name

