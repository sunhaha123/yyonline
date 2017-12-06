# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 15:12:47 2017

@author: Administrator
"""

from  django.conf.urls import url, include

from  .views import  OrgView,AddUserAskView
from  .views import TeacherListView,TeacherDetailView,AddFavView,OrgHomeView

urlpatterns = [
#     课程机构列表页
    url(r'^list/$',OrgView.as_view(),name="org_list"),
    # url(r'add_ask/$',AddUserAskView().as_view(),name="add_ask" ),
    url(r'^add_ask/$', AddUserAskView.as_view(), name="add_ask"),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="org_home"),
    # 机构收藏
    url(r'^add_fav/$', AddFavView.as_view(), name="add_fav"),

    # 讲师列表页
    url(r'^teacher/list/$', TeacherListView.as_view(), name="teacher_list"),
    # 教练详情页
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name="teacher_detail"),
    # url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name="teacher_detail"),
]