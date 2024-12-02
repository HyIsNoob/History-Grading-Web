from django.contrib import admin
from .models import exam_exam, exam_question, exam_answerkey, exam_answer, exam_primarykey
# Register your models here.

class examAdmin(admin.ModelAdmin):
    list_display = ['title', 'max_point', 'create', 'eid']
    search_fields = ['title']
admin.site.register(exam_exam, examAdmin)

class answerAdmin(admin.ModelAdmin):
    list_display = ['qid', 'uid', 'point']
admin.site.register(exam_answer, answerAdmin)

class AKAdmin(admin.ModelAdmin):
    list_display = ['qid', 'key']
admin.site.register(exam_answerkey, AKAdmin)

admin.site.register(exam_primarykey)

class questionAdmin(admin.ModelAdmin):
    list_display = ['eid', 'max_point', 'title', 'qid', 'cauhoi']
admin.site.register(exam_question, questionAdmin)
