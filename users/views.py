from django.shortcuts import render, redirect
from django.contrib import messages

#   定义一个注册的视图函数
from users.forms import RegisteForm

# Create your views here.

def registe(request):
    if request.method == 'GET':
        #get请求，展示表单数据
        form = RegisteForm()
    else:
        #post请求，添加注册的用户到数据库中，展示表单信息
        form = RegisteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, '注册成功~！')
            return redirect('/')
    return render(request, 'form.html', context={
        'form': form,
        'little_title': '注册用户'
    })


#
def success(request):
    msg = request.GET.get('msg')
    messages.add_message(request, messages.SUCCESS, msg)
    return redirect('/')