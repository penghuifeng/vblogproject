from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import Post, Category, Student
from .forms import StudentForm, StudentModelForm, CommentModelForm
import markdown
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# 定义首页的视图函数
def index(request):
    # return HttpResponse('首页')
    #  1.获取分页参数：页码page_num、每页记录数
    page_num = request.GET.get('page_num', 1)
    page_size = request.GET.get('page_size', 2)
    # 2. 把所有文章查出来
    post_all = Post.objects.all().order_by('-created_time')
    #  3.实例化分页器Paginator对象
    try:
        p = Paginator(post_all, page_size)
    except ValueError:
        #如果page_size不是整数， 那么我们就指定默认每页2条数据
        p = Paginator(post_all, 2)
    #  4.得到特页的数据
    try:
        post_list = p.page(page_num)
        # 如果页面不是整数 int型 ， 那么返回第一页的数据
    except PageNotAnInteger:
        post_list = p.page(1)

    except EmptyPage:
        #  如果页码太大， 超过最大页，这时候我们就返回最后一页的数据
        post_list = p.page(p.num_pages)
    #  5. 使用特定页的文章数据进行页面的渲染
    return render(request, 'blog/index.html', context={'post_list': post_list})


def detail(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == 'GET':
        post.add_views()
        form = CommentModelForm()
        # 1. GET:渲染页面
    else:
        # 2.POST:添加数据、渲染错误的页面
        form = CommentModelForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            # return HttpResponse('添加评论成功')
            # 1. 添加评论
            messages.add_message(request, messages.SUCCESS, '添加评论成功~')

            return redirect('/posts/{}/'.format(id))
        else:
            messages.add_message(request, messages.ERROR, '输入有误，请重新输入~')
    return render(request, 'blog/detail.html', {
        'post': post,
        'form': form
    })

# 定义归档的视图函数
def archives(request, year, month):
    # year 2021 month 10
    # 去数据库里面把created_time的年份等于2021年 月份等于10月 的文章数据查出来
    post_list = Post.objects.filter(
        created_time__year=year, created_time__month=month).order_by('-created_time')
    return render(request, 'blog/index.html', context={
        'post_list': post_list
    })

# 定义分类的视图函数
def categories(request, id):
    # id 1
    # 数据库里面把 id等于1的类别下的所有文章查出来
    ## 方式一：
    # post_list = Post.objects.filter(category__id=id).order_by('-created_time')
    ## 方式二：
    category = get_object_or_404(Category, id=id)
    post_list = Post.objects.filter(category=category).order_by('-created_time')
    return render(request, 'blog/index.html', context={
        'post_list': post_list
    })

#搜索页面
# def search(request):
#     print(request)
#     return HttpResponse('搜索页面')

def search(request):
    keyword = request.GET.get('wd','')
    # 需求
    # keywords: python java
    # 去查询文章的数据，只要文章的标题或者文章的内容中包含该关键字就把该文章查出来
    post_list = Post.objects.filter(
        Q(title__contains=keyword) | Q(body__contains=keyword)).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

def page1(request):
    return render(request, 'test/page1.html')

def page2(request):
    return render(request, 'test/page2.html')

def form1(request):
    #如果请求是 GET：返回表单
    print(request.method)
    if request.method == 'GET':
        return render(request, 'test/form1.html')
    else:
        print(request)
        #如果请求是POST： 接收用户记录， 往数据库中插入记录
        #  1. 用来接收用户在表单 中输入的 数据
        name = request.POST.get('name', '')
        age = request.POST.get('age', 0)
        print(name, age)
        # 2.  通过模型把数据插入数据库中
        student = Student(name=name, age=age)
        student.save()
        return HttpResponse('添加成功')

def form2(request):
    if request.method == 'GET':
        #如果请求是get， 返回表单页面
        form = StudentForm()
    else:
        form = StudentForm(request.POST)
        if form.is_valid():
            name = form.data.get('name', '')
            age = form.data.get('age', 0)
            student = Student(name=name, age=age)
            student.save()
            return HttpResponse('添加成功')
    return render(request, 'test/form2.html', context={
        'form': form
    })

def form3(request):
    print(request.method)
    if request.method == 'GET':
        form = StudentModelForm()
    #如果请求是POST， 进行数据添加
    else:
        form = StudentModelForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('添加数据成功')
    return render(request, 'test/form3.html', context={
        'form': form
    })