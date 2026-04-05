from os import pardir
from typing import List
from django import http
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from numpy import add, where
from . models import exam_exam, exam_question
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from . forms import addkeyword, quesedit, thembai, addcauhoi, deleteques, themlop
from . import Scoring, tfidf
from django.shortcuts import redirect
import mysql.connector
import datetime
import json
import underthesea
from underthesea import word_tokenize, pos_tag
import logging    # first of all import the module

logging.basicConfig(filename='std.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.warning('This message will get logged on to a file')

#Show Bài Tập
class BTListView(ListView):
    queryset = exam_exam.objects.all().order_by('-eid')
    template_name = 'baitap/baitap.html'
    context_object_name = 'baitapp'
    paginate_by = 3
class BTDetailView(DetailView):
    model = exam_question
    template_name = 'baitap/baitap.html'
#Show Câu Hỏi
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
#Lưu Câu Hỏi
def savecauhoi(request):
    if request.method == "POST":
        #kết nối đến DB (Để thông tin giống như ở Django DB/Admin)
        mydb = mysql.connector.connect(
            host="localhost",
            user="khanghy1102",
            password="1102",
            database="DeadDB"
            )
        
        mycursor = mydb.cursor()

        #biến sql chứa lệnh cần thực thi
        sql = "INSERT INTO baitap_exam_question (max_point, title, description, eid_id, answergv, cauhoi, `key`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        #sql = "INSERT INTO tên_bảng (giá_trị_1, giá_trị_2, ... , giá_trị_N) VALUES (%s, %s, ..., %s)"
        #data cần catch khi request đến
        d_maxpoint = request.POST.get('max_point', '')
        d_title = request.POST.get('title', '')
        d_description = request.POST.get('description', '')
        d_eid = request.POST.get('eid', '')
        d_answer = request.POST.get('answergv', '')
        d_cauhoi = request.POST.get('cauhoi', '')
        d_key = request.POST.get('key', '')
        
        #data cần push lên DB, mỗi giá trị/biến tương ứng với %s ở lệnh trong biến sql ở trên
        val = (d_maxpoint, d_title, d_description, d_eid, d_answer, d_cauhoi, str(d_key))
        mycursor.execute(sql, val)
        mydb.commit()
        
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
    else:
        return HttpResponse('<script>alert("Lỗi post")</script>')
#Edit câu hỏi
def addkey(request, qid):
    mydb = mysql.connector.connect(
        host="localhost",
        user="khanghy1102",
        password="1102",
        database="DeadDB"
            )
            
    mycursor = mydb.cursor()
    sql1 = "SELECT * FROM `baitap_exam_question` WHERE qid='%s'"
    val = (qid,)
    mycursor.execute(sql1, val)
    myresult1 = mycursor.fetchall()
    my_list1 = myresult1
    my_dict1 = dict() 
    for index,value1 in enumerate(my_list1):
        my_dict1[index] = value1
    s = quesedit()
    context = {"qid":qid, "q":my_dict1, "s":s}
    return render(request, 'baitap/quesedit.html', context)
#Lưu edit câu hỏi
def savekeyword(request):
    if request.method == "POST":
        b = quesedit(request.POST)
        if b.is_valid():
            mydb = mysql.connector.connect(
                host="localhost",
                user="khanghy1102",
                password="1102",
                database="DeadDB"
                )
            
            mycursor = mydb.cursor()

            sql = "UPDATE baitap_exam_question SET max_point = %s, title = %s, description = %s, answergv = %s, cauhoi = %s, `key` = %s WHERE qid = %s"
            d_maxpoint = request.POST.get('max_point', '')
            d_title = request.POST.get('title', '')
            d_description = request.POST.get('description', '')
            d_answer = request.POST.get('answergv', '')
            d_cauhoi = request.POST.get('cauhoi', '')
            d_key = request.POST.get('keyword', '')
            d_qid = request.POST.get('qid', '')
            
            #data cần push lên DB, mỗi giá trị/biến tương ứng với %s ở lệnh trong biến sql ở trên
            val = (d_maxpoint, d_title, d_description, d_answer, d_cauhoi, str(d_key), d_qid)
            mycursor.execute(sql, val)
            mydb.commit()
            return HttpResponseRedirect('/editdone/')
        else:
            return HttpResponse('<script>alert("Lỗi valid")</script>')
    else:
        return HttpResponse('<script>alert("Lỗi post")</script>')


#Xoá Câu Hỏi
def quesdelconf(request, id):
    eid = request.POST.get('eid', '')
    return render(request, 'baitap/delexam.html', {'id':id, 'eid': eid})
def deleteques(request):
    s = addcauhoi()
    mydb = mysql.connector.connect(
        host="localhost",
        user="khanghy1102",
        password="1102",
        database="DeadDB"
        )

    mycursor = mydb.cursor()

            #biến sql chứa lệnh cần thực thi
    sql = "DELETE FROM baitap_exam_question WHERE `qid` = %s"
    d_id = request.POST.get('qid', '')
    val = (d_id,)
    mycursor.execute(sql, val)
    mydb.commit()
    eid = request.POST.get('eid', '')
    return HttpResponseRedirect('/baitap/%s/' %eid)
    

#Xoá Bài KT
def exdelconf(request, id):
    return render(request, 'baitap/delques.html', {'id':id})
def examdelete(request):
    s = thembai()
    mydb = mysql.connector.connect(
        host="localhost",
        user="khanghy1102",
        password="1102",
        database="DeadDB"
        )

    mycursor = mydb.cursor()

            #biến sql chứa lệnh cần thực thi
    sql = "DELETE FROM baitap_exam_exam WHERE `eid` = %s"
    d_id = request.POST.get('eid','')
    val = (d_id,)
    mycursor.execute(sql, val)

    mydb.commit()
    #myArray = JSON.Parse(context)
    
    return HttpResponseRedirect('/baitap/')
#Lưu và Chấm Bài
def save_nopbai(request, id):
    if request.method == "POST":
        mydb = mysql.connector.connect(
            host="localhost",
            user="khanghy1102",
            password="1102",
            database="DeadDB"
            )
        mycursor = mydb.cursor()
        
        sql = "SELECT * FROM `baitap_exam_question` WHERE eid_id=%s"
        val = (id,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        for tupl1 in myresult:
            x = []
            for y in tupl1:
                x.append(y)
            MACAUHOI = x[0]
            DAPAN = x[5]
            CAUTRALOi = request.POST.get('answer','')
            input1 = DAPAN
            input2 = CAUTRALOi
            sql2 = "SELECT `key` FROM baitap_exam_question WHERE qid = %s"
            val = (MACAUHOI,)
            mycursor.execute(sql2, val) 
            myresult3 = mycursor.fetchall()
            def convertTuple(tup):
                str = ''
                for item in tup:
                    if item == None:
                        pass
                    else:
                        str = str + item
                return str
            def listToString(s): 
                str1 = ""  
                for ele in s: 
                    str1 += ele   
                return str1 
            for z in myresult3:
                a = convertTuple(z)
                list = pos_tag(a)
                maxdem = 0
                dem = 0
                for bac in list:
                    ronglist = []
                    chu = bac[0]
                    loai = bac[1]
                    if loai == "CH" or loai == "C":
                        pass
                    elif loai != "CH" and loai != "C":
                        ronglist.append(bac[0])
                        maxdem += 1
                        pui = listToString(ronglist)
                        so = pui.lower()
                        sanh = input2.lower()
                        if so in sanh:
                            dem += 1
                input_1 = input1
                input_2 = input2
                print(input_1, input_2)
                modelVersion = 0 
                model = Scoring.MakeModel(0)
                POINT = Scoring.similarity(model, input_1, input_2)*10
                LastPoint = (dem/maxdem)*2 + POINT*0.8
                Key = (dem/maxdem)*2
                UpPointAI = round(POINT, 2)
                UpKey = round(Key, 2)
                UpPoint = round(LastPoint, 2)
                if myresult3 == '':
                    UpPoint = UpPointAI
                    UpKey = ''
                sql = "INSERT INTO baitap_exam_answer (answer, point, pointai, pointkey, qid_id, uid_id, `create`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                d_create = datetime.datetime.now()
                d_ques = MACAUHOI
                d_user = request.POST.get('uid', '')
                val = (CAUTRALOi, str(UpPoint), str(UpPointAI), str(UpKey), d_ques, d_user, str(d_create),)
                mycursor.execute(sql, val)
                mydb.commit()
                context = {'Score':UpPoint, 'AIP': UpPointAI, 'KeyP': UpKey}
            return render(request, 'baitap/save.html', context)
    else:
        return HttpResponse('<script>alert("Lỗi post")</script>')
#Thêm bài kt
def them_bai(request):
    s = thembai()
    context = {'f' : s}
    return render(request, 'baitap/thembai.html', context)
#Thêm Lớp
def them_lop(request):
    #<button class='btn btn-success'  onclick='window.location.href="{% url "themlop" %}"'>Thêm Lớp Học</button></center>
    mydb = mysql.connector.connect(
        host="localhost",
        user="khanghy1102",
        password="1102",
        database="DeadDB"
            )
            
    mycursor = mydb.cursor()
    sql1 = "SELECT * FROM `baitap_lophocbehind`"

    mycursor.execute(sql1)
    myresult1 = mycursor.fetchall()
    my_list1 = myresult1
    my_dict1 = dict() 
    for index,value1 in enumerate(my_list1):
        my_dict1[index] = value1

    sql = "SELECT * FROM `user_customeruser`"

    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    my_list = myresult
    my_dict = dict() 
    for index,value in enumerate(my_list):
        my_dict[index] = value

    s = themlop()
    context = {'f' : s, "q":my_dict1, "a": my_dict}
    return render(request, 'baitap/addclass.html', context)
#Lưu Lớp Mới
def save_lop(request):
    if request.method == "POST":
        b = themlop(request.POST)
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
            sql = "INSERT INTO baitap_lophoc (lophoc, sohocsinh, lop, uid_id) VALUES (%s, %s, %s, %s)"
            #sql = "INSERT INTO tên_bảng (giá_trị_1, giá_trị_2, ... , giá_trị_N) VALUES (%s, %s, ..., %s)"
            #data cần catch khi request đến
            d_lophoc = request.POST.get('lophoc', '')
            d_sohocsinh = request.POST.get('sohocsinh', '')
            d_lop = request.POST.get('lop', '')
            d_uid = request.POST.get('uid', '')

            #data cần push lên DB, mỗi giá trị/biến tương ứng với %s ở lệnh trong biến sql ở trên
            val = (d_lophoc, d_sohocsinh, d_lop, d_uid)
            mycursor.execute(sql, val)
            mydb.commit()
            context = {"f": b}
            return HttpResponseRedirect('/baitap/', context)
        else:
            return HttpResponse('<script>alert("Lỗi valid")</script>')
    else:
        return HttpResponse('<script>alert("Lỗi post")</script>')
#Lưu bài KT mới
def save_exam(request):
    if request.method == "POST":
        mydb = mysql.connector.connect(
            host="localhost",
            user="khanghy1102",
            password="1102",
            database="DeadDB"
            )
        
        mycursor = mydb.cursor()

        #biến sql chứa lệnh cần thực thi
        sql = "INSERT INTO baitap_exam_exam (max_point, title, description, take, code, uid_id, time, start_time, end_time, `create`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        #sql = "INSERT INTO tên_bảng (giá_trị_1, giá_trị_2, ... , giá_trị_N) VALUES (%s, %s, ..., %s)"
        #data cần catch khi request đến
        d_maxpoint = request.POST.get('max_point', '')
        d_title = request.POST.get('title', '')
        d_description = request.POST.get('description', '')
        d_take = request.POST.get('take', '')
        d_code = request.POST.get('code', '')
        d_uid = request.POST.get('uid', '')
        d_time = request.POST.get('time', '')
        d_st = request.POST.get('start_time', '')
        d_et = request.POST.get('end_time', '')
        d_create = datetime.datetime.now()

        #data cần push lên DB, mỗi giá trị/biến tương ứng với %s ở lệnh trong biến sql ở trên
        val = (d_maxpoint, d_title, d_description, d_take, d_code, d_uid, d_time, d_st, d_et, d_create)
        mycursor.execute(sql, val)
        mydb.commit()
        return HttpResponseRedirect('/baitap/')
    else:
        return HttpResponse('<script>alert("Lỗi post")</script>')
#Thêm Câu Hỏi
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
#Xem điểm
def viewdiem(request, uid):
    mydb = mysql.connector.connect(
        host="localhost",
        user="khanghy1102",
        password="1102",
        database="DeadDB"
        )     
    mycursor1 = mydb.cursor()
    #lấy ra câu trả lời theo id của câu hỏi
    sql2 = "SELECT * FROM `baitap_exam_answer` WHERE qid_id ='%s'"
    val2 = (uid,)
    mycursor1.execute(sql2, val2)
    myresult2 = mycursor1.fetchall()

    sql3 = "SELECT * FROM `baitap_exam_question` WHERE qid ='%s'"
    val3 = (uid,)
    mycursor1.execute(sql3, val3)
    myresult3 = mycursor1.fetchall()

    for x in myresult3:
        eid = x[4]
    my_list1 = myresult2
    my_dict1 = dict() 
    for index,value1 in enumerate(my_list1):
        my_dict1[index] = value1
    context = {'f': my_dict1, 'b': myresult2, 'id': uid, 'eid': eid}
    return render(request, 'baitap/viewdiem.html', context)
#Xem profile người nộp
def profileshow(request, id):
    mydb = mysql.connector.connect(
        host="localhost",
        user="khanghy1102",
        password="1102",
        database="DeadDB"
        )     
    mycursor1 = mydb.cursor()
    #lấy ra câu trả lời theo id của câu hỏi
    sql2 = "SELECT * FROM `user_customeruser` WHERE uid ='%s'"
    val2 = (id,)
    mycursor1.execute(sql2, val2)
    myresult2 = mycursor1.fetchall()
    my_list1 = myresult2
    my_dict1 = dict() 
    for index,value1 in enumerate(my_list1):
        my_dict1[index] = value1
    context = {'f': my_dict1, 'b': myresult2, 'uid': id}
    return render(request, 'baitap/profileshow.html', context)

#xoá câu trả lời
def ansdelconf(request, id):
    qid = request.POST.get('qid', '')
    return render(request, 'baitap/delans.html', {'id':id, 'qid': qid})
def ansdelete(request):
    mydb = mysql.connector.connect(
        host="localhost",
        user="khanghy1102",
        password="1102",
        database="DeadDB"
        )

    mycursor = mydb.cursor()

            #biến sql chứa lệnh cần thực thi
    sql = "DELETE FROM baitap_exam_answer WHERE `aid` = %s"
    d_id = request.POST.get('aid','')
    val = (d_id,)
    mycursor.execute(sql, val)

    mydb.commit()
    #myArray = JSON.Parse(context)
    qid = request.POST.get('qid','')
    return HttpResponseRedirect('/baitap/viewdiem/%s/' %qid)

#Chỉnh sửa câu hỏi
def editques(request):
    if request.method == "POST":
        mydb = mysql.connector.connect(
            host="localhost",
            user="khanghy1102",
            password="1102",
            database="DeadDB"
            )
        mycursor = mydb.cursor()
        sql = "UPDATE baitap_exam_question SET max_point = %s, title = %s, description = %s, answergv = %s, cauhoi = %s, `key` = %s WHERE qid = %s"
        d_maxpoint = request.POST.get('max_point', '')
        d_title = request.POST.get('title', '')
        d_description = request.POST.get('description', '')
        d_answergv = request.POST.get('answergv', '')
        d_cauhoi = request.POST.get('cauhoi', '')
        d_key = request.POST.get('key', '')
        d_qid = request.POST.get('qid1', '')

        val = (d_maxpoint, d_title, d_description, d_answergv, d_cauhoi, d_key, d_qid,)
        mycursor.execute(sql, val)
        mydb.commit()
        eid = request.POST.get('eid1', '')
        return HttpResponseRedirect('/baitap/%s/' %eid)
    else:
        return HttpResponse('<script>alert("Lỗi post")</script>')
#Chỉnh sửa bài kiểm tra
def editexam(request, id):
    
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
    
    for x in myresult1:
        pass
    context = {'eid': id, 'tt': x[2], 'mp': x[1], 'des': x[3], 'st': x[4], 'et': x[5], 'take': x[6], 'time': x[7], 'code': x[8],}
    return render(request, 'baitap/examedit.html', context)
#Lưu chỉnh sửa bài kiểm tra
def saveeditexam(request, id):
    if request.method == "POST":
        mydb = mysql.connector.connect(
            host="localhost",
            user="khanghy1102",
            password="1102",
            database="DeadDB"
            )
        
        mycursor = mydb.cursor()

        sql = "UPDATE baitap_exam_exam SET max_point = %s, title = %s, description = %s, take = %s, max_point = %s, `code` = %s, `start_time` = %s, `end_time` = %s, `time` = %s     WHERE eid = %s"
        d_maxpoint = request.POST.get('max_point', '')
        d_title = request.POST.get('title', '')
        d_description = request.POST.get('description', '')
        d_take = request.POST.get('take', '')
        d_mp = request.POST.get('max_point', '')
        d_code = request.POST.get('code', '')
        d_st = request.POST.get('start_time', '')
        d_et = request.POST.get('end_time', '')
        d_time = request.POST.get('time', '')
        eid = id
        
        #data cần push lên DB, mỗi giá trị/biến tương ứng với %s ở lệnh trong biến sql ở trên
        val = (d_maxpoint, d_title, d_description, d_take, d_mp, d_code, d_st, d_et, d_time, eid)
        mycursor.execute(sql, val)
        mydb.commit()
        return HttpResponseRedirect('/baitap/')
    else:
        return HttpResponse('<script>alert("Lỗi post")</script>')