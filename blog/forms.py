from django import forms
from .models import Student, Post, Comment

#定义了一个django的学生表单类
class StudentForm(forms.Form):
    name = forms.CharField(label='名字', required=True, max_length=3)
    age = forms.IntegerField(label='年龄', min_value=0, max_value=200)


class StudentModelForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'age']

class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'url', 'text']

#post增删改查----添加一个文章的模型表单
class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = []