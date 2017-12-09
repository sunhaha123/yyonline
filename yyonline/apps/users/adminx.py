# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 15:12:47 2017

@author: Administrator
"""
import  xadmin
from xadmin import  views
from  xadmin.plugins.auth import  UserAdmin
from  xadmin.layout import Main ,Side, Row, Fieldset

from  .models import EmailVerifyRecord,UserProfile
from  .models import Banner


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

class GloabalSettings(object):
    site_title = "云鸟网"
    site_footer = "云鸟网"
    menu_style = "accordion"

class EmailVerifyRecordAdmin(object):
    list_display = ['code','email','send_type','send_time']
    search_fields = ['code','email','send_type']
    list_filter = ['code','email','send_type','send_time']

class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index','add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index','add_time']

# class UserAdmin(object):
#     list_display = ['username', 'nick_name', 'last_login', 'email']
#     search_fields = ['username', 'nick_name', 'last_login', 'email']
#     list_filter = ['username', 'nick_name', 'last_login', 'email']


xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
# xadmin.site.register(UserProfile,UserAdmin)
# xadmin.site.register(UserProfile,UserProfileAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GloabalSettings)