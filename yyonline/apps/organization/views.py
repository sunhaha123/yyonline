# -*- coding:utf-8 -*-
from django.shortcuts import render
from  django.views.generic import  View
from  django.http import HttpResponse,HttpRequest,HttpResponseRedirect
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .models import CourseOrg,CityDict,Teacher
from  .form import UserAskForm
from  courses.models import  Course
from  operation.models import UserFavorite
from  courses.models import Course

# Create your views here.


class OrgView(View):
    """
    课程机构列表功能
    """
    def get(self,request):
        all_orgs = CourseOrg.objects.all()
        all_citys = CityDict.objects.all()
        # 机构搜索
        search_keywords = request.GET.get('keywords', "")
        # like 语句（i不区分大小写）
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))
        return  render(request,"org-list.html",{
            "all_orgs":all_orgs,
            "all_citys":all_citys,
            # "org_nums":org_nums,
            # "city_id":city_id,
            # "category":category,
            # "hot_orgs":hot_orgs,
            # "sort":sort,
        })

class AddUserAskView(View):
    """
    用户添加咨询
    """
    def post(self,request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            return  HttpResponse('{"status":"fail","msg":"添加出错"}',content_type='application/json')

class OrgHomeView(View):
    """
    机构首页
    """
    def get(self,request,org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request,'org-detail-homepage.html',{
            "all_courses":all_courses,
            "all_teachers":all_teachers,
            "course_org":course_org,
        })

class TeacherListView(View):
       """
       课程教练列表
       """
       def get(self, request):
           all_teachers = Teacher.objects.all()
           # return render(request,"teachers-list.html",{
           #      "all_teachers":all_teachers,
           #  })

           search_keywords = request.GET.get('keywords', "")
           # like 语句（i不区分大小写）
           if search_keywords:
               all_teachers = all_teachers.filter(Q(name__icontains=search_keywords)|
                                              Q(work_company__icontains=search_keywords)|
                                              Q(work_position__icontains=search_keywords))

           # 排序
           sort = request.GET.get("sort", "")
           if sort:
               if sort == "hot":
                   all_teachers = all_teachers.order_by("-click_nums")

           sorted_teacher = Teacher.objects.all().order_by("-click_nums")[:3]

            # 对讲师进行分页
           try:
               page = request.GET.get('page', 1)
           except PageNotAnInteger:
               page = 1
               # Provide Paginator with the request object for complete querystring generation
           t=all_teachers.count()
           p = Paginator(all_teachers,1, request=request)
           teachers = p.page(page)
           return render(request, "teachers-list.html", {
               "all_teachers": teachers,
               "sorted_teacher": sorted_teacher,
               "sort": sort,
               # "current_nav": current_nav,
               "count_teacher":t,

           })



class AddFavView(View):
    """
    用户收藏
    """
    def post(self,request):
        fav_id = request.POST.get("fav_id", 0)
        fav_type = request.POST.get("fav_type", 0)

        if not request.user.is_authenticated():
            """
            此处user为一个匿名类，django内置的一种方法，此user与正常的user有相似的用法
            所以此处调用user.is_authenticated()方法，后面带括号.
            """
            return HttpResponse('{"status": "fail", "msg":"用户未登录"}', content_type="application/json")

        exit_recods = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exit_recods:
            """
            记录已经存在，则表示要取消收藏
            """
            exit_recods.delete()
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums <= 0:
                    course.fav_nums =0
                course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums -= 1
                if course_org.fav_nums <= 0:
                    course_org.fav_nums = 0
                course_org.save()

            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums <= 0:
                    teacher.fav_nums = 0
                teacher.save()

            return HttpResponse('{"status": "success", "msg":"收藏"}', content_type="application/json")
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()

                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()

                return HttpResponse('{"status": "success", "msg":"已收藏"}', content_type="application/json")
            else:
                return HttpResponse('{"status": "fail", "msg":"收藏出错"}', content_type="application/json")

class TeacherDetailView(View):
    def get(self,request,teacher_id):
        if not request.user.is_authenticated():
            """
            此处user为一个匿名类，django内置的一种方法，此user与正常的user有相似的用法
            所以此处调用user.is_authenticated()方法，后面带括号.
            """
            from django.core.urlresolvers import reverse
            return HttpResponseRedirect(reverse("login"))
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums+=1
        all_courses = Course.objects.filter(teacher=teacher)

        has_teacher_faved = False
        if UserFavorite.objects.filter(user=request.user,fav_type=3,fav_id=teacher_id):
            has_teacher_faved = True

        has_org_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
            has_org_faved = True

        #讲师排行
        sorted_teacher = Teacher.objects.all().order_by("-click_nums")[:3]
        return render(request,"teacher-detail.html",{
            "teacher":teacher,
            "all_courses":all_courses,
            "sorted_teacher":sorted_teacher,
            "has_teacher_faved":has_teacher_faved,
            "has_org_faved": has_org_faved,
        })