from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User

# Register your models here.


#定义用户管理器
class MyUserAdmin(UserAdmin):
    def __init__(self, *args, **kwargs):
        super(MyUserAdmin, self).__init__(*args, **kwargs)
        self.list_display += ('nickname',)
        self.add_fieldsets[0][1]['fields'] += ('nickname',)
        self.fieldsets[1][1]['fields'] += ('nickname',)


#注册模型到管理系统时，使用上用户管理器
admin.site.register(User, MyUserAdmin)