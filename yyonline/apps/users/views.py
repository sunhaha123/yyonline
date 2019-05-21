# -*- coding:utf-8 -*-
import json
from django.shortcuts import render
from  django.contrib.auth import  authenticate,login,logout
from  django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from  django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.hashers import make_password

from  .models import UserProfile,Banner,EmailVerifyRecord
from .form import LoginForm,UploadImageForm,ModifyPwdForm,UserProfile,UserInfoForm,RegisterForm
from  utils.mixin_utils import LoginRequireMixin
from operation.models import UserCourse,UserFavorite
from  organization.models import CourseOrg,Teacher
from  courses.models import Course
from utils.email_send import send_register_email

# Create your views here.
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class ActiveUserView(View):
    def get(self,request,active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request,"register.html",{
            "register_form":register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)

            send_register_email(user_name, "register")
            user_profile.save()
            return render(request, "login.html")
        else:
            return render(request, "register.html",{"register_form":register_form})

class LoginView(View):
    def get(self,request):
        return render(request, "login.html",{})
    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
              if user.is_active:
                 login(request, user)
                 from django.core.urlresolvers import reverse
                 return HttpResponseRedirect(reverse("index"))
              else:
                  return render(request, "login.html", {"msg": "用户未激活,请到邮箱激活！"})
            else:
                return render(request, "login.html", {"msg": "用户名或者密码错误！"})
        else:
            return render(request, "login.html",{"login_form":login_form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse("index"))

class UserinfoView(LoginRequireMixin,View):
    """
    用户个人信息
    """
    def get(self,request):
        return  render(request,'usercenter-info.html',{})
    def post(self,request):
        user_info_form = UserInfoForm(request.POST,instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(LoginRequireMixin,View):
    """
    用户修改头像
    """
    def post(self,request):
        image_form = UploadImageForm(request.POST,request.FILES)
        if image_form.is_valid():
            image = image_form.cleaned_data['image']
            request.user.image=image
            request.user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')

class UpdatePwdView(View):
    """
    个人中心修改用户密码
    """
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            # email = request.POST.get("email")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()

            return  HttpResponse('{"status":"success","msg":"修改成功"}', content_type='application/json')
        else:

            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')

class MyCourseView(LoginRequireMixin,View):
    """
    我的课程
    """
    def  get(self,request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request,'usercenter-mycourse.html',{
            "user_courses":user_courses,
        })

class MyFavOrgView(LoginRequireMixin,View):
    """
    我的课程
    """
    def  get(self,request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user,fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id= org_id)
            org_list.append(org)
        return render(request,'usercenter-fav-org.html',{
            "org_list":org_list,
        })

class MyFavTeacherView(LoginRequireMixin,View):
    """
    我的教练
    """
    def  get(self,request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user,fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id= teacher_id)
            teacher_list.append(teacher)
        return render(request,'usercenter-fav-teacher.html',{
            "teacher_list":teacher_list,
        })

class MyFavCourseView(LoginRequireMixin,View):
    """
    我的教练
    """
    def  get(self,request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user,fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id= course_id)
            course_list.append(course)
        return render(request,'usercenter-fav-course.html',{
            "course_list":course_list,
        })

class IndexView(View):
    """
    首页
    """
    def get(self, request):
        all_banners = Banner.objects.all().order_by("index")
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:10]

        return render(request, "index.html", {
            "all_banners": all_banners,
            "courses": courses,
            "banner_courses": banner_courses,
            "course_orgs": course_orgs,
        })