# -*- coding: utf-8 -*-
from django.shortcuts import render
from  django.views.generic import  View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from keras.models import load_model
netfile = "media/tmp/net_0.h5"
model = load_model(netfile)
import numpy as np
model.predict(np.zeros((2,50,9)))
import pandas as pd

import time

from  .models import Course,Sensor
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
        if not request.user.is_authenticated():
            """
            此处user为一个匿名类，django内置的一种方法，此user与正常的user有相似的用法
            所以此处调用user.is_authenticated()方法，后面带括号.
            """
            from django.core.urlresolvers import reverse
            return HttpResponseRedirect(reverse("login"))
        course = Course.objects.get(id=int(course_id))
        #增加课程点击数
        course.click_nums +=1
        course.save()

        tag = course.tag
        if tag:
            relate_course = Course.objects.filter(tag=tag)[:1]
        else:
            relate_course = []

        sensor = Sensor.objects.get(id=19)
        return render(request,"course-detail.html",{
            "course":course,
            "relate_course":relate_course,
            "sensor":sensor,

        })

class CourseD2View(View):
    def post(self, request,course_id):
        if request.method == "POST":    # 请求方法为POST时，进行处理
            myFile =request.FILES.get("myfile", None)    # 获取上传的文件，如果没有文件，则默认为None
            if not myFile:
                return HttpResponse("no files for upload!")
            # text = myFile.read()
            import matplotlib
            matplotlib.use('TkAgg')
            import matplotlib.pyplot as plt

            matplotlib.rcParams['font.sans-serif'] = ['SimHei']
            matplotlib.rcParams['font.family'] = 'sans-serif'
            matplotlib.rcParams['axes.unicode_minus'] = False
            data0 = pd.read_table(myFile, delim_whitespace=True)
            #
            f = data0.plot()
            Id = request.user.id
            Int = int(time.time())
            path1 =  "sensor/examples%d.jpg"%Int
            path2 = "media/"+path1
            plt.savefig(path2)
            f.clear()
            plt.close()
            image_data = open(path2, "rb").read()
            sensor = Sensor()
            sensor.image = path1


            course = Course.objects.get(id=int(course_id))
            # 增加课程点击数
            course.click_nums += 1
            course.save()

            tag = course.tag
            if tag:
                relate_course = Course.objects.filter(tag=tag)[:1]
            else:
                relate_course = []

            # sensor = Sensor.objects.get(id=2)

            #处理数据
            data1 = pd.read_table('media/tmp/腰准备降重心.txt', delim_whitespace=True)
            data2 = pd.read_table('media/tmp/腰准备动作没降重心.txt', delim_whitespace=True)
            data3 = pd.concat([data1,data2],axis=0)
            from sklearn import preprocessing
            scaler = preprocessing.StandardScaler().fit(data3)
            df = scaler.transform(data0)
            df = pd.DataFrame(df)
            n_prev = 50
            # from keras.utils.np_utils import to_categorical
            import numpy as np
            docX, docY = [], []
            for i in range(0, len(df) - n_prev, 25):
                docX.append(df.iloc[i:i + n_prev].as_matrix())
            alsX = np.array(docX)
            netfile = "media/tmp/net_0.h5"
            # from keras.models import load_model
            # model = load_model(netfile)
            # import numpy as np
            # model.predict(np.zeros((2,50,9)))
            global model
            y_pred = model.predict(alsX).round()
            pred = y_pred[0][25][0]
            #category to 类别
            if pred == 1:
                sensor.category = "重心下降标准"
            else:
                sensor.category = "重心未下降标准"
            sensor.user = request.user
            sensor.save()

            return render(request,"course-detail2.html",{
                "course":course,
                "relate_course":relate_course,
                "sensor":sensor,

            })
            #
            # destination = open(os.path.join("G:\\upload",myFile.name),'wb+')    # 打开特定的文件进行二进制的写操作
            # for chunk in myFile.chunks():      # 分块写入文件
            #     destination.write(chunk)
            # destination.close()
            # return HttpResponse("upload over!")
