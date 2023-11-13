from django import template
from blog.models import Post,Category

register = template.Library()

@register.inclusion_tag('test/hello.html', takes_context=True)
def say_hello(context):
    return {
        'msg': '欢迎使用我们的博客网站aaa'
    }

# 定义用来展示最新文章的模板标签的函数
@register.inclusion_tag('blog/inclusions/recent_posts.html', takes_context=True)
def show_recent_posts(context):
    return {
        'recent_posts': Post.objects.all().order_by('-created_time')[:3]
    }

# 定义用来展示归档内容的模板标签的函数
@register.inclusion_tag('blog/inclusions/archives.html', takes_context=True)
def show_archives(context):
    return {
        'archives': Post.objects.dates('created_time', 'month', order='DESC')
    }

# 定义用来展示分类内容的模板标签的函数
@register.inclusion_tag('blog/inclusions/categories.html', takes_context=True)
def show_categories(context):
    return {
        'categories': Category.objects.all()
    }