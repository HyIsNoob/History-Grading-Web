from typing import List
from django import http
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from numpy import where
from . models import exam_exam, exam_question
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from . forms import nopbai, thembai, themques
from . import Scoring, tfidf
from django.shortcuts import redirect
import mysql.connector
import datetime
import json

# Create your views here.
class BTListView(ListView):
    queryset = exam_exam.objects.all().order_by('eid')
    template_name = 'baitap/baitap.html'
    context_object_name = 'baitapp'
    paginate_by = 3


class BTDetailView(DetailView):
    model = exam_question
    template_name = 'baitap/baitap.html'

def examinfor(id):
    #kết nối đến DB (Để thông tin giống như ở Django DB/Admin)
    
    mydb = mysql.connector.connect(
        host="localhost",
        user="khanghy1102",
        password="1102",
        database="DeadDB"
        )     
    mycursor1 = mydb.cursor()


    sql1 = "SELECT * FROM `baitap_exam_exam` WHERE eid='%s'"


    val = (id,)
    mycursor1.execute(sql1, val)

    myresult1 = mycursor1.fetchall()

    context = {'infor': myresult1}
    #myArray = JSON.Parse(context)
    return context

def questionlist(request, id):
    #kết nối đến DB (Để thông tin giống như ở Django DB/Admin)

    mydb = mysql.connector.connect(
        host="localhost",
        user="khanghy1102",
        password="1102",
        database="DeadDB"
        )     
    mycursor1 = mydb.cursor()

    sql1 = "SELECT * FROM `baitap_exam_question` WHERE eid_id='%s'"

    val = (id,)
    mycursor1.execute(sql1, val)

    myresult1 = mycursor1.fetchall()

    #myArray = JSON.Parse(context)
    sql1 = "SELECT * FROM `baitap_exam_exam` WHERE eid='%s'"


    val = (id,)
    mycursor1.execute(sql1, val)

    myresult2 = mycursor1.fetchall()

    context = {'infor': myresult2, 'f': myresult1}
    
    return render(request, 'baitap/quesview.html', context)
    
    
def examdelete(request, id):
    s = thembai()
    mydb = mysql.connector.connect(
        host="localhost",
        user="khanghy1102",
        password="1102",
        database="DeadDB"
        )
            
    mycursor = mydb.cursor()

            #biến sql chứa lệnh cần thực thi
    sql = "DELETE FROM baitap_exam_exam WHERE eid = '%s'"
    val = (id,)
    mycursor.execute(sql, val)

    mydb.commit()
    #myArray = JSON.Parse(context)
    
    return render(request, 'baitap/delexam.html', {'s':s})


class QuesDetailView(DetailView):
    model = exam_question
    template_name = 'baitap/quesview.html'

def quesdetail(request, id):
    detail = exam_question.objects.get(eid=3)
    noidung = exam_question.objects.all()
    baitap = exam_exam.objects.get(eid=id)
    #context_object_name = 'baitapp'
    context = {'question': detail,'noidung': noidung,'baitap':baitap}
    return render(request, 'baitap/quesview.html', context)

def add_nopbai(request):
    s = nopbai()
    context = {'f' : s}
    return render(request, 'baitap/nopbai.html', context)

def save_nopbai(request):
    if request.method == "POST":
        b = nopbai(request.POST)
        if b.is_valid():
            modelVersion = 0 
            model = Scoring.MakeModel(0)
            text_1 = open("baitap/example/doc_1.txt", "r", encoding = "utf8").read().lower()
            text_2 = request.POST["answer"].lower()
            Score = Scoring.similarity(model, text_1, text_2)*10
            
            #kết nối đến DB (Để thông tin giống như ở Django DB/Admin)
            mydb = mysql.connector.connect(
                host="localhost",
                user="khanghy1102",
                password="1102",
                database="DeadDB"
                )
            
            mycursor = mydb.cursor()

            #biến sql chứa lệnh cần thực thi
            sql = "INSERT INTO baitap_exam_answer (answer, point, qid_id, uid_id) VALUES (%s, %s, %s, %s)"
            #sql = "INSERT INTO tên_bảng (giá_trị_1, giá_trị_2, ... , giá_trị_N) VALUES (%s, %s, ..., %s)"
            #data cần catch khi request đến
            d_ques = request.POST.get('qid', '')
            d_user = request.POST.get('uid', '')
            d_body = request.POST.get('answer', '')
            d_diem = round(Score, 2)
            #d_create = datetime.datetime.now()

            #data cần push lên DB, mỗi giá trị/biến tương ứng với %s ở lệnh trong biến sql ở trên
            val = (d_body, str(d_diem), d_ques, d_user)
            mycursor.execute(sql, val)
            mydb.commit()
            context = {"Score": round(Score, 2), "f": b}
            return render(request, 'baitap/save.html', context)
        else:
            return HttpResponse('<script>alert("Lỗi valid")</script>')
    else:
        return HttpResponse('<script>alert("Lỗi post")</script>')

def cham_bai(request):
    pass

def them_bai(request):
    s = thembai()
    context = {'f' : s}
    return render(request, 'baitap/thembai.html', context)

def save_exam(request):
    if request.method == "POST":
        b = thembai(request.POST)
        if b.is_valid():
            #kết nối đến DB (Để thông tin giống như ở Django DB/Admin)
            mydb = mysql.connector.connect(
                host="localhost",
                user="khanghy1102",
                password="1102",
                database="DeadDB"
                )
            
            mycursor = mydb.cursor()

            #biến sql chứa lệnh cần thực thi
            sql = "INSERT INTO baitap_exam_exam (max_point, title, description, take, code, uid_id, time, create) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
            #sql = "INSERT INTO tên_bảng (giá_trị_1, giá_trị_2, ... , giá_trị_N) VALUES (%s, %s, ..., %s)"
            #data cần catch khi request đến
            d_maxpoint = request.POST.get('max_point', '')
            d_title = request.POST.get('title', '')
            d_description = request.POST.get('description', '')
            d_take = request.POST.get('take', '')
            d_code = request.POST.get('code', '')
            d_uid = request.POST.get('uid', '')
            d_time = str(datetime.datetime.now())
            d_create = str(datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y"))

            #data cần push lên DB, mỗi giá trị/biến tương ứng với %s ở lệnh trong biến sql ở trên
            val = (d_maxpoint, d_title, d_description, d_take, d_code, d_uid, d_time, d_create)
            mycursor.execute(sql, val)
            mydb.commit()
            context = {"f": b}
            return HttpResponseRedirect('/baitap/', context)
        else:
            return HttpResponse('<script>alert("Lỗi valid")</script>')
    else:
        return HttpResponse('<script>alert("Lỗi post")</script>')

def addques(request,id):
    if request.method == "POST":
        b = themques(request.POST)
        if b.is_valid():
            #kết nối đến DB (Để thông tin giống như ở Django DB/Admin)
            mydb = mysql.connector.connect(
                host="localhost",
                user="khanghy1102",
                password="1102",
                database="DeadDB"
                )
            
            mycursor = mydb.cursor()

            #biến sql chứa lệnh cần thực thi
            sql = "INSERT INTO baitap_exam_question (max_point, title, description, eid_id) VALUES (%s, %s, %s, %s)"
            #sql = "INSERT INTO tên_bảng (giá_trị_1, giá_trị_2, ... , giá_trị_N) VALUES (%s, %s, ..., %s)"
            #data cần catch khi request đến
            d_maxpoint = request.POST.get('max_point', '')
            d_title = request.POST.get('title', '')
            d_description = request.POST.get('description', '')
            d_eid = request.POST.get(id,)
            
            #data cần push lên DB, mỗi giá trị/biến tương ứng với %s ở lệnh trong biến sql ở trên
            val = (d_maxpoint, d_title, d_description, d_eid)
            mycursor.execute(sql, val)
            mydb.commit()
            context = {"f": b}
            return HttpResponseRedirect('/baitap/{{id}}', context)
        else:
            return HttpResponse('<script>alert("Lỗi valid")</script>')
    else:
        return HttpResponse('<script>alert("Lỗi post")</script>')
