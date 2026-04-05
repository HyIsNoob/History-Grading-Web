from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import RegisForm, roleUser, updateUser
from django.shortcuts import redirect
import mysql.connector
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'pages/home.html')

def contact(request):
    return render(request, 'pages/contact.html')

def error(request, exception):
    return render(request, 'pages/error.html', {'message': exception})

def register(request):
    form = RegisForm()
    if request.method == 'POST':
        form = RegisForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login/')
    return render(request, 'pages/register.html', {'form' : form})

def nopbai(request):
    return render(request, 'pages/nopbai.html')

def profile(request):
    mydb = mysql.connector.connect(
        host="localhost",
        user="khanghy1102",
        password="1102",
        database="DeadDB"
            )
            
    mycursor = mydb.cursor()
    sql1 = "SELECT * FROM `baitap_lophoc`"

    mycursor.execute(sql1)
    myresult1 = mycursor.fetchall()
    my_list1 = myresult1
    my_dict1 = dict() 
    for index,value1 in enumerate(my_list1):
        my_dict1[index] = value1
    context = {"q":my_dict1,}
    return render(request, 'pages/profile.html', context)

def add_profile(request):
    s = updateUser()
    context = {'f' : s}
    return render(request, 'pages/addprofile.html', context)

def update_profile(request):
    if request.method == "POST":
        u = updateUser(request.POST)
        if u.is_valid():
            mydb = mysql.connector.connect(
            host="localhost",
            user="khanghy1102",
            password="1102",
            database="DeadDB"
            )
                    
            mycursor = mydb.cursor()

            sql = "UPDATE user_customeruser SET stt = %s, lop = %s, school = %s, phone_number = %s, email = %s, first_name = %s WHERE username = %s"
            
            d_fn = request.POST.get('firstname','')
            d_stt = request.POST.get('stt', '')
            d_lop = request.POST.get('lop', '')
            d_school = request.POST.get('school', '')
            d_phonenumber = request.POST.get('phone_number', '')
            d_email = request.POST.get('email', '')
            d_user = request.POST.get('user', '')

            val = (d_stt, d_lop, d_school, d_phonenumber, d_email, d_fn, d_user)
            mycursor.execute(sql, val)
            mydb.commit()
            return render(request, 'pages/profile.html')
        else:
            return HttpResponse('<script>alert("Lỗi valid")</script>')
    else:
        return HttpResponse('<script>alert("Lỗi post")</script>')

def roleselect(request):
    return render(request, 'pages/roleselect.html')

def rolegv(request):
    if request.method == "POST":
        r = roleUser(request.POST)
        if r.is_valid():
            mydb = mysql.connector.connect(
            host="localhost",
            user="khanghy1102",
            password="1102",
            database="DeadDB"
            )
                    
            mycursor = mydb.cursor()
            
            sql = "UPDATE user_customeruser SET role = %s WHERE username = %s"
            
            d_role = request.POST.get('role', '')
            d_user = request.POST.get('user', '')

            val = (d_role, d_user)
            mycursor.execute(sql, val)
            mydb.commit()
            return render(request, 'pages/profile.html')
        else:
            return HttpResponse('<script>alert("Lỗi valid")</script>')
    else:
        return HttpResponse('<script>alert("Lỗi post")</script>')

