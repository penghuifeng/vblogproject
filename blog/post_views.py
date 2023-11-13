from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.db.models import Q
from blog.models import Post
from blog.forms import PostModelForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.contrib import messages
def post_list(request):
    # /post/list/?page_num=1&page_size=2&keyword=python
    # 1.获取 查询字符串中的分页参数   和  查询关键字参数
    page_num = request.GET.get('page_num', 1)
    page_size = request.GET.get('page_size', 2)
    keyword = request.GET.get('keyword', '')

    # 2. 把文章中标题或内容包含关键字keyword的文章查出来
    post_all = Post.objects.filter(
        Q(title__contains=keyword) | Q(body__contains=keyword))
    # 3. 创建一个分页器
    try:
        p = Paginator(post_all, page_size)
    except ValueError:
        # 如果page_size不是整数， 那么我们就指定默认每页2条数据
        p = Paginator(post_all, 2)
    # 4. 利用分页器得到特定页的数据
    try:
        post_list = p.page(page_num)
        # 如果页面不是整数 int型 ， 那么返回第一页的数据
    except PageNotAnInteger:
        post_list = p.page(1)

    except EmptyPage:
        #  如果页码太大， 超过最大页，这时候我们就返回最后一页的数据
        post_list = p.page(p.num_pages)

    #  5. 使用特定页的文章数据进行页面的渲染
    return render(request, 'post/list.html', context={
        'post_list': post_list
    })

def post_add(request):
    if request.method == 'GET':
        #get请求， 展示表单
        form = PostModelForm()
    else:
        # Post 请求， 添加数据
        form = PostModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, '添加文章成功')
            return redirect('/post/list/')

    return render(request, 'post/add.html', context={
        'form': form
    })

def post_edit(request, id):
    #利用id把特定的文章查出来
    post = get_object_or_404(Post, id=id)
    if request.method == 'GET':
        #get请求，展示表单
        form = PostModelForm(instance=post)
    else:
        #post请求，编辑数据、展示错误的表单
        form = PostModelForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, '编辑成功~')
            return redirect('/post/list/')
    return render(request, 'post/edit.html', context={
        'form': form
    })


def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    messages.add_message(request, messages.SUCCESS, '删除文章成功！')
    return redirect('/post/list')