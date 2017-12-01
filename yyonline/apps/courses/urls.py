# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 15:12:47 2017

@author: Administrator
"""
from  django.conf.urls import url, include
from .views import CourseListView,CourseDetailView,Upload_FileView

urlpatterns = [
#     课程机构列表页
    url(r'^list/$',CourseListView.as_view(),name="course_list"),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),


]