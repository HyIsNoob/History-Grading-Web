from django.contrib import admin
from .models import CustomerUser
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'role', 'stt', 'lop', 'school', 'phone_number']
    search_fields = ['role']
admin.site.register(CustomerUser, UserAdmin)