from baitap.forms import nopbai
from django.urls import path
from . import views

urlpatterns = [
  path('', views.BTListView.as_view(), name='baitap'),
  path('<int:id>/', views.questionlist, name='quesview'),
  path('save/', views.save_nopbai, name='save'),
  path('ketqua/', views.cham_bai, name='cb1'),
  path('delete/<int:id>/',views.examdelete, name='delexam'),
  path('thembai/', views.them_bai, name='thembai'),
  path('saveex/', views.save_exam, name='saveex'),
  path('deleteques/<int:id>/', views.deleteques, name='deleteques'),
  path('saveques/', views.savecauhoi, name='saveques'),
  path('delques/<int:id>/',views.donedelques, name='donedelques'),
  #path('addques/', views.addques, name='addques'),
]




