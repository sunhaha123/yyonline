# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 15:12:47 2017

@author: Administrator
"""
from .models import Course, activityID, SportData
import xadmin


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image',
                    'click_nums', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums',
                   'add_time']


# class LessonAdmin(object):
#     list_display = ['course', 'name', 'add_time']
#     search_fields = ['course', 'name']
#     # course 是一个对象，xadmin 不能搜索，需要指定搜索 course 对象里哪一个属性
#     list_filter = ['course__name', 'name', 'add_time']
#
#
class SportDataAdmin(object):
    list_display = [ 'user', 'sportid','type','position','data_x','data_y','data_z','rate','action_time',]
    search_fields = ['user', 'sportid','type','data_x','data_y','data_z','rate','action_time','position',]
    list_filter = ['user', 'sportid','type','data_x','data_y','data_z','rate','action_time','position',]

#
class activityIDAdmin(object):
    list_display = [ 'id','name',]
    search_fields = [ 'id','name']
    list_filter = ['id', 'name']


xadmin.site.register(Course, CourseAdmin)
# xadmin.site.register(SportData, LessonAdmin)
xadmin.site.register(SportData, SportDataAdmin)
xadmin.site.register(activityID, activityIDAdmin)