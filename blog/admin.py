from django.contrib import admin
from .models import Category, Tag, Post, Student, Comment

# 把模型注册到管理系统中
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Student)
admin.site.register(Comment)