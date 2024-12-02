from baitap.forms import nopbai
from django.urls import path
from . import views

urlpatterns = [
  path('', views.BTListView.as_view(), name='baitap'),
  path('<int:id>/', views.questionlist, name='quesview'),
  path('nopbai/', views.add_nopbai, name='nopbai'),
  path('save/', views.save_nopbai, name='save'),
  path('ketqua/', views.cham_bai, name='cb1'),
  path('delete/<int:id>/',views.examdelete, name='delexam'),
  path('thembai/', views.them_bai, name='thembai'),
  path('saveex/', views.save_exam, name='saveex'),
  path('addques/<int:id>/', views.addques, name='themques'),
]




