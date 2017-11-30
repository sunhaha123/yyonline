# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 15:12:47 2017

@author: Administrator
"""

from  django.conf.urls import url, include

from .views import  UserinfoView,UploadImageView,UpdatePwdView,MyCourseView,MyFavOrgView,MyFavTeacherView,MyFavCourseView,IndexView

urlpatterns = [
#     用户信息
    url(r'^info/$',UserinfoView.as_view(),name="user_info"),
    # url(r'add_ask/$',AddUserAskView().as_view(),name="add_ask" ),
    #用户头像上传
    url(r'^image/upload/$',UploadImageView.as_view(),name="image_upload"),
    #用户个人中心密码修改
    url(r'^update/pwd/$',UpdatePwdView.as_view(),name="update_pwd"),
    #我的课程
    url(r'^mycourse/$',MyCourseView.as_view(),name="mycourse"),
    #我收藏的机构
    url(r'^myfav/org/$',MyFavOrgView.as_view(),name="myfav_org"),
    #我收藏的老师
    url(r'^myfav/teacher/$',MyFavTeacherView.as_view(),name="myfav_teacher"),
    #我收藏的课程
    url(r'^myfav/course/$',MyFavCourseView.as_view(),name="myfav_course"),


]