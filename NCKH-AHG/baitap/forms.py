from django import forms
from django.forms import fields, widgets
from . models import exam_answer, exam_exam, exam_question, exam_answerkey, lophoc


#class nopbai(forms.ModelForm):
#    class Meta:
#        model = exam_answer
#        fields = ('answer', 'qid', 'uid',)
#        widgets = {
#            'answer': widgets.Textarea(attrs={'id':'noidung', 'cols':'100'}),
#        }


class thembai(forms.ModelForm):
    class Meta:
        model = exam_exam
        fields = ('title','description','take','max_point','code','uid', 'start_time', 'end_time', 'time')
        widgets = {
            'title': widgets.Input(attrs={'id':'title'}),
            'description': widgets.Textarea(attrs={'id':'description'}),
            'max_point': widgets.Input(attrs={'id':'max_point'}),
            'take': widgets.Input(attrs={'id':'take'}),
            'code': widgets.Input(attrs={'id':'code'}),
            'uid': widgets.Input(attrs={'id':'uid'}),
            'start_time': widgets.Input(attrs={'id':'st'}),
            'end_time': widgets.Input(attrs={'id':'et'}),
            'time': widgets.Input(attrs={'name':'time', 'id':'time'}),
        }



class themlop(forms.ModelForm):
    class Meta:
        model = lophoc
        fields = ('lophoc','sohocsinh',)
        widgets = {
            'lophoc': widgets.Input(attrs={'id':'lophoc'}),
            'sohocsinh': widgets.Textarea(attrs={'id':'sohocsinh'}),
        }



class addcauhoi(forms.ModelForm):
    class Meta:
        model = exam_question
        fields = ('max_point', 'title', 'description', 'eid', 'cauhoi', 'answergv',)
        widgets = {
            'title': widgets.Input(attrs={'id':'title', 'cols':'100', 'rows':"10"}),
            'description': widgets.Textarea(attrs={'id':'description', 'cols':'100'}),
            'max_point': widgets.Input(attrs={'id':'max_point'}),
            'eid': widgets.Input(attrs={'id':'eid'}),
            'cauhoi': widgets.Input(attrs={'id':'cauhoi'}),
            'answergv': widgets.Input(attrs={'id':'answergv'}),
        }


class deleteques(forms.ModelForm):
    class meta:
        model = exam_question
        fields = ('qid',)
        widgets = {
            'qid': widgets.Input(attrs={'id': 'qid'})
        }


class quesedit(forms.ModelForm):
    class Meta:
        model = exam_question
        fields = ('max_point', 'title', 'description', 'answergv', 'cauhoi','key',)


class addkeyword(forms.ModelForm):
    class meta:
        model = exam_answerkey
        fields = ('key', 'qid',)
        widgets = {
            'key': widgets.Input(attrs={'id': 'key'}),
            'qid': widgets.Input(attrs={'id': 'qid'})
        }



    