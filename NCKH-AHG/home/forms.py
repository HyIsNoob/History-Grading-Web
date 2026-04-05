from django import forms
import re 
from user.models import CustomerUser
from django.contrib.auth.models import Group, User
from django.core.exceptions import ObjectDoesNotExist
from django.forms.fields import ChoiceField
from django import forms
from django.core.files.images import get_image_dimensions
from django.forms import widgets

class RegisForm(forms.Form):
    username = forms.CharField(label='Tài khoản', max_length=30)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Nhập lại mật khẩu', widget=forms.PasswordInput())
    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2 and password1:
                return password2
        raise forms.ValidationError("Mật khẩu không hợp lệ")
    def clean_username(self):
        username = self.cleaned_data['username']
        if re.search(r'^\w+&@!#$%* ', username):
            raise forms.ValidationError("Tên tài khoản có kí tự đặc biệt")
        try:
            CustomerUser.objects.get(username=username)
        except CustomerUser.DoesNotExist:
            return username
        raise forms.ValidationError("Tài khoản đã tồn tại")
    def save(self):
        CustomerUser.objects.create_user(username=self.cleaned_data['username'], email=self.cleaned_data['email'], password=self.cleaned_data['password1'])

#forms.py
class updateUser(forms.ModelForm):
    class Meta:
        model = CustomerUser
        fields = ('stt', 'lop', 'school', 'phone_number', 'email', 'first_name')

class roleUser(forms.ModelForm):
    class Meta:
        model = CustomerUser
        fields = ('role',)
