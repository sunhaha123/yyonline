# -*- coding:utf-8 -*-
"""yyonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from  django.views.generic import TemplateView
import  xadmin
from django.views.static import serve
from yyonline.settings import MEDIA_ROOT

from  users.views import LoginView
from  organization.views import OrgView


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),

    url('^$',TemplateView.as_view(template_name="index.html"),name="index"),
    url('^login/$', LoginView.as_view(), name="login"),
    url('^logout/$', LoginView.as_view(), name="logout"),

#    课程机构首页
    url(r'^org/', include('organization.urls', namespace="org")),
    # 配置上传文件
    url(r'^media/(?P<path>.*)$', serve, {"document_root":MEDIA_ROOT}),
    # 课程列表
    url(r'^course/', include('courses.urls', namespace="course")),
    # 用户
    url(r'^users/', include('users.urls', namespace="users")),

]
