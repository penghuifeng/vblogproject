from django.urls import path

from blogproject import settings
from users import views
from django.contrib.auth import views as auth_views
from users.forms import AuthForm

SUCCESS_URL = '/success/?msg='


urlpatterns = [
    path('registe/', views.registe),
    path('success/', views.success),

    path('login/', auth_views.LoginView.as_view(
        form_class = AuthForm,
        extra_context = {'little_title': '用户登录'},
        template_name = 'form.html'
    )),
    path('logout/', auth_views.LogoutView.as_view(
        next_page = SUCCESS_URL + '退出成功!'
    )),
    path('password/change/', auth_views.PasswordChangeView.as_view(
        title = settings.TITLE,
        template_name = 'form.html',
        extra_context = {'little_title': '修改密码'},
        success_url = SUCCESS_URL + '修改成功~'
    )),
    path('password/reset/', auth_views.PasswordResetView.as_view(
        title = settings.TITLE,
        extra_context = {'little_title': '重置密码'},
        template_name = 'form.html',
        email_template_name = 'users/password_reset_email.html',
        success_url = SUCCESS_URL + '发送邮箱重置密码成功！',
    )),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        title = settings.TITLE,
        extra_context = {'little_title': '输入新密码'},
        template_name = 'form.html',
        success_url = SUCCESS_URL + '恭喜~密码重置成功！！'
    ))
]