from django.urls import path
from . import views

urlpatterns = [
  path('', views.BTListView.as_view(), name='baitap'),
  path('<int:id>/', views.questionlist, name='quesview'),
  path('save/<int:id>/', views.save_nopbai, name='save'),
  path('deleteex/<int:id>/',views.exdelconf, name='delexam'),
  path('deleteques/<int:id>/',views.quesdelconf, name='delques'),
  path('deleteans/<int:id>/',views.ansdelconf, name='deleteans'),
  path('deleteyes/', views.examdelete, name='examdelete'),
  path('deletequesyes/', views.deleteques, name='deleteques'),
  path('deleteansyes/', views.ansdelete, name='deleteansyes'),
  path('thembai/', views.them_bai, name='thembai'),
  path('themlop/', views.them_lop, name='themlop'),
  path('savelop/', views.save_lop, name='savelop'),
  path('saveex/', views.save_exam, name='saveex'),
  path('saveques/', views.savecauhoi, name='saveques'),
  path('quesedit/<int:qid>/', views.addkey, name='keyword'),
  path('viewdiem/<int:uid>/', views.viewdiem, name='viewdiem'),
  path('editques/', views.editques, name='editques'),
  path('editexam/<int:id>/', views.editexam, name='editexam'),
  path('saveeditexam/<int:id>/', views.saveeditexam, name='saveeditexam'),
  path('profileshow/<int:id>/', views.profileshow, name='profileshow'),
]




