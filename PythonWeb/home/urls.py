from django.urls import path
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
   path('', views.index, name='index'),
   path('profile/', views.profile, name='profile'),
   path('contact/', views.contact, name='contact'),
   path('register', views.register, name="register"),
   path('login/',auth_views.LoginView.as_view(template_name="pages/login.html"), name="login"),
   path('logout/',auth_views.LogoutView.as_view(next_page='/'),name='logout'),
   path('nopbai/', views.nopbai, name='nopbai'),
   path('update/', views.add_profile, name='addprofile'),
   path('updateprofile/', views.update_profile, name='updateprofile'),
   path('rolegv/', views.rolegv, name='rolegv'),
   path('roleselect/', views.roleselect, name='roleselect'),
]

