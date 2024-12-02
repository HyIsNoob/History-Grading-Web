from typing import List
from django import http
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from numpy import add, where
from . models import exam_exam, exam_question
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from . forms import nopbai, thembai, addcauhoi, deleteques, editques
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
    paginate_by = 5


class BTDetailView(DetailView):
    model = exam_question
    template_name = 'baitap/baitap.html'


def questionlist(request, id):
    #kết nối đến DB (Để thông tin giống như ở Django DB/Admin)

    mydb = mysql.connector.connect(
        host="localhost",
        user="khanghy1102",
        password="1102",
        database="DeadDB"
        )     
    mycursor1 = mydb.cursor()
    #maxpoint
    sql1 = "SELECT * FROM `baitap_exam_question` WHERE eid_id='%s'"
    val = (id,)
    mycursor1.execute(sql1, val)
    myresult1 = mycursor1.fetchall()

    #myArray = JSON.Parse(context)
    sql = "SELECT * FROM `baitap_exam_exam` WHERE eid='%s'"
    val = (id,)
    mycursor1.execute(sql, val)
    myresult2 = mycursor1.fetchall()

    my_list1 = myresult2
    my_dict1 = dict() 
    for index,value1 in enumerate(my_list1):
        my_dict1[index] = value1

    if myresult1 == '':
        my_dict = ''
    
    else:
        my_list = myresult1
        my_dict = dict() 
        for index,value in enumerate(my_list):
            my_dict[index] = value
    s = addcauhoi()
    context = {'eid': id, 's': my_dict, 'f': my_dict1, 'b': myresult1, 'u':s}
    return render(request, 'baitap/quesview.html', context)

def savecauhoi(request):
    if request.method == "POST":
        a = addcauhoi(request.POST)
        if a.is_valid():
            #kết nối đến DB (Để thông tin giống như ở Django DB/Admin)
            mydb = mysql.connector.connect(
                host="localhost",
                user="khanghy1102",
                password="1102",
                database="DeadDB"
                )
            
            mycursor = mydb.cursor()

            #biến sql chứa lệnh cần thực thi
            sql = "INSERT INTO baitap_exam_question (max_point, title, description, eid_id, answergv, cauhoi) VALUES (%s, %s, %s, %s, %s, %s)"
            #sql = "INSERT INTO tên_bảng (giá_trị_1, giá_trị_2, ... , giá_trị_N) VALUES (%s, %s, ..., %s)"
            #data cần catch khi request đến
            d_maxpoint = request.POST.get('max_point', '')
            d_title = request.POST.get('title', '')
            d_description = request.POST.get('description', '')
            d_eid = request.POST.get('eid', '')
            d_answer = request.POST.get('answergv', '')
            d_cauhoi = request.POST.get('cauhoi', '')
            
            #data cần push lên DB, mỗi giá trị/biến tương ứng với %s ở lệnh trong biến sql ở trên
            val = (d_maxpoint, d_title, d_description, d_eid, d_answer, d_cauhoi,)
            mycursor.execute(sql, val)
            mydb.commit()
            context = {"f": a}
            return HttpResponseRedirect('/baitap/', context)
        else:
            return HttpResponse('<script>alert("Lỗi valid")</script>')
    else:
        return HttpResponse('<script>alert("Lỗi post")</script>')

def quesdelete(request, id):
    s = deleteques()
    mydb = mysql.connector.connect(
        host="localhost",
        user="khanghy1102",
        password="1102",
        database="DeadDB"
        )
            
    mycursor = mydb.cursor()

            #biến sql chứa lệnh cần thực thi
    sql = "DELETE FROM baitap_exam_question WHERE qid = '%s'"
    val = (id,)
    mycursor.execute(sql, val)

    mydb.commit()
    #myArray = JSON.Parse(context)
    
    return render(request, 'baitap/delexam.html', {'s':s})

def addeditques(request,id):
    s = editques()
    context = {'a':s}
    return render(request, 'baitap/editques.html', context)

def donedelques(request, id):
    return render(request, '/baitap/delques.html' , {'id': id})
def deleteques(request, id):
    s = addcauhoi()
    mydb = mysql.connector.connect(
        host="localhost",
        user="khanghy1102",
        password="1102",
        database="DeadDB"
        )

    mycursor = mydb.cursor()

            #biến sql chứa lệnh cần thực thi
    sql = "DELETE FROM baitap_exam_question WHERE qid = %s"
    val = (id,)
    mycursor.execute(sql, val)

    mydb.commit()
    #myArray = JSON.Parse(context)
    
    return render(request, 'baitap/delexam.html', {'s':s})

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
    
    return render(request, 'baitap/delques.html', {'s':s})

def save_nopbai(request):
    if request.method == "POST":
        b = nopbai(request.POST)
        if b.is_valid():

            mydb = mysql.connector.connect(
                host="localhost",
                user="khanghy1102",
                password="1102",
                database="DeadDB"
                )
            
            mycursor = mydb.cursor()

            #sql = "SELECT answergv FROM `baitap_exam_question` WHERE qid=7"
            #val = (id,)
            #mycursor.execute(sql)
            #mydb.commit()
            #myresult = mycursor.fetchall()
            #my_list = myresult
            #my_dict = dict() 
            #for index,value in enumerate(my_list):
            #    my_dict[index] = value

            modelVersion = 0 
            model = Scoring.MakeModel(0)
            text_1 = open("baitap/example/doc_1.txt", "r", encoding = "utf8").read().lower()
            text_2 = request.POST["answer"].lower()
            Score = Scoring.similarity(model, text_1, text_2)*10
            
            #kết nối đến DB (Để thông tin giống như ở Django DB/Admin)
            

            #biến sql chứa lệnh cần thực thi
            sql1 = "INSERT INTO baitap_exam_answer (answer, point, qid_id, uid_id) VALUES (%s, %s, %s, %s)"
            #sql = "INSERT INTO tên_bảng (giá_trị_1, giá_trị_2, ... , giá_trị_N) VALUES (%s, %s, ..., %s)"
            #data cần catch khi request đến
            d_ques = request.POST.get('qid', '')
            d_user = request.POST.get('uid', '')
            d_body = request.POST.get('answer', '')
            d_diem = round(Score, 2)
            #d_create = datetime.datetime.now()

            #data cần push lên DB, mỗi giá trị/biến tương ứng với %s ở lệnh trong biến sql ở trên
            val = (d_body, str(d_diem), d_ques, d_user)
            mycursor.execute(sql1, val)
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
            sql = "INSERT INTO baitap_exam_exam (max_point, title, description, take, code, uid_id, time, start_time, end_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            #sql = "INSERT INTO tên_bảng (giá_trị_1, giá_trị_2, ... , giá_trị_N) VALUES (%s, %s, ..., %s)"
            #data cần catch khi request đến
            d_maxpoint = request.POST.get('max_point', '')
            d_title = request.POST.get('title', '')
            d_description = request.POST.get('description', '')
            d_take = request.POST.get('take', '')
            d_code = request.POST.get('code', '')
            d_uid = request.POST.get('uid', '')
            d_time = datetime.datetime.now()
            d_st = request.POST.get('start_time', '')
            d_et = request.POST.get('end_time', '')

            #data cần push lên DB, mỗi giá trị/biến tương ứng với %s ở lệnh trong biến sql ở trên
            val = (d_maxpoint, d_title, d_description, d_take, d_code, d_uid, d_time, d_st, d_et)
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
            sql = "SELECT * FROM `baitap_exam_exam` WHERE eid='%s'"
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
        
        return HttpResponse('<script>alert("Lỗi POST")</script>')

def themques(request,eid):
    data_qs = exam_exam.objects.filter(eid=eid).values('title','description')
    data_qs1 = exam_question.objects.filter(eid=eid).values('title','description','max_point','answergv')
    for data in data_qs:
        title = data['title']
        description = data['description']
    if data_qs1 == '':
        title1 = ''
        description1 = ''
        max_point = ''
        answer = ''
    else: 
        for datar in data_qs1:    
            title1 = datar['title']
            description1 = datar['description']
            max_point = datar['max_point']
            answer = datar['answergv']
    context = {"f":data_qs1, "eid": eid, "title": title, "description": description, "maxpoint": max_point, "answer": answer, "title1": title1, "description1": description1}
    return render(request, 'baitap/themques.html', context)
