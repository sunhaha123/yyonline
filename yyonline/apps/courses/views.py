# -*- coding: utf-8 -*-
from django.shortcuts import render
from  django.views.generic import  View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from  .models import Course
# Create your views here.

class CourseListView(View):
    def get(self,request):
        all_courses = Course.objects.filter(is_banner=False).order_by("-add_time")

        hot_courses = Course.objects.filter(is_banner=False).order_by("-students")[:3]
        #课程搜索
        search_keywords = request.GET.get('keywords' ,"" )
        # like 语句（i不区分大小写）
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)|Q(detail__icontains=search_keywords),is_banner=False)
        # 排序
        sort = request.GET.get("sort", "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")


        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
            # Provide Paginator with the request object for complete querystring generation
        t = all_courses.count()
        p = Paginator(all_courses, 2, request=request)
        courses = p.page(page)
        return render(request,'course-list.html',{
            "all_courses":courses,
            "sort":sort,
            "hot_courses":hot_courses,

        })

class CourseDetailView(View):
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        #增加课程点击数
        course.click_nums +=1
        course.save()

        tag = course.tag
        if tag:
            relate_course = Course.objects.filter(tag=tag)[:1]
        else:
            relate_course = []
        return render(request,"course-detail.html",{
            "course":course,
            "relate_course":relate_course,

        })