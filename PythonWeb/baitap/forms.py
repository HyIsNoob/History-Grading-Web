from django import forms
from django.forms import fields, widgets
from . models import exam_answer, exam_exam, exam_question


class nopbai(forms.ModelForm):
    class Meta:
        model = exam_answer
        fields = ('answer', 'point')
        widgets = {
            'answer': widgets.Textarea(attrs={'id':'noidung', 'cols':'100'}),
        }


class thembai(forms.ModelForm):
    class Meta:
        model = exam_exam
        fields = ('title','description','take','max_point','code','uid',)
        widgets = {
            'title': widgets.Input(attrs={'id':'title', 'cols':'100', 'rows':"10"}),
            'description': widgets.Textarea(attrs={'id':'description', 'cols':'100'}),
            'max_point': widgets.Input(attrs={'id':'max_point'}),
            'take': widgets.Input(attrs={'id':'take'}),
            'code': widgets.Input(attrs={'id':'code'}),
            'uid': widgets.Input(attrs={'id':'uid'}),
        }

class themques(forms.ModelForm):
    class Meta:
        model = exam_question
        fields = ('max_point', 'title', 'description', 'eid',)
        widgets = {
            'title': widgets.Input(attrs={'id':'title', 'cols':'100', 'rows':"10"}),
            'description': widgets.Textarea(attrs={'id':'description', 'cols':'100'}),
            'max_point': widgets.Input(attrs={'id':'max_point'}),
            'eid': widgets.Input(attrs={'id':'eid'}),
        }



    