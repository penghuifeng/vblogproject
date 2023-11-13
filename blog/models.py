from django.contrib.auth.models import User
from django.db import models

import markdown
from django.utils.html import strip_tags
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension

from users.models import User

# 1. 创建文章分类的模型类
class Category(models.Model):
    # 添加类名名称的字段
    name = models.fields.CharField('分类名称', max_length=100)

    class Meta:
        verbose_name = '文章分类'   # 单数形式
        verbose_name_plural = verbose_name    # 复数形式

    def __str__(self):
        return '{}-{}'.format(self.id, self.name)


# 2. 创建文章标签的模型类
class Tag(models.Model):
    # 添加名称的字段
    name = models.fields.CharField('标签名称', max_length=100)

    class Meta:
        verbose_name = '文章标签'   # 单数形式
        verbose_name_plural = verbose_name    # 复数形式

    def __str__(self):
        return self.name

# 3. 创建文章的模型类
class Post(models.Model):
    title = models.fields.CharField('文章标题', max_length=100)
    body = models.fields.TextField('文章内容')
    body_html = models.fields.TextField('文章内容html形式', editable=False)
    toc_html =models.fields.TextField('文章目录html形式', editable=False)

    # auto_now_add=True  会把添加的时间，作为created_time的时间值
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    # auto_now=True 会把添加的时间和往后修改记录的时间，作为modified_time的时间值
    modified_time = models.DateTimeField('修改时间', auto_now=True)

    # 就是在文章表中添加分类的外键，指定该文章属于什么分类
    # on_delete=models.CASCADE   级联删除
    #     级联删除的意思时当把类别删除时把该类别的文章都删除
    category = models.ForeignKey(Category, verbose_name = '类别', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name = '标签')
    author = models.ForeignKey(User, verbose_name = '作者', on_delete=models.CASCADE)

    # 摘要
    excerpt = models.CharField('摘要', max_length=64, editable=False)
    # 阅读次数
    # editable=False 指定该字段不能在管理系统进行编辑
    views = models.PositiveIntegerField('阅读次数', default=0, editable=False)

    class Meta:
        verbose_name = '文章'   # 单数形式
        verbose_name_plural = verbose_name    # 复数形式

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # TODO: 自动生成摘要
        # 1. 把md的文本内容转换成html的字符串
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            TocExtension(slugify=slugify)
        ])
        self.body_html = md.convert(self.body)
        self.toc_html = md.toc
        # 2. 把html的字符串中html标签通过strip_tags给剔除掉
        # 3. 提取出前54个字符串作为摘要的内容
        self.excerpt = strip_tags(self.body_html)[:54]
        super().save(*args, **kwargs)

    def add_views(self):
        self.views += 1
        self.save()


#4.创建学生的模型类
class Student(models.Model):
    #添加类名称的字段
    name = models.fields.CharField('名字', max_length=100)
    age = models.fields.IntegerField('年龄')

    class Meta:
        verbose_name = '学生'  #单数形式
        verbose_name_plural = verbose_name #复数形式

    def __str__(self):
        return '{}-{}'.format(self.id, self.name)


#4. 添加评论的模型
class Comment(models.Model):
    name = models.fields.CharField('名字', max_length=32)
    email = models.fields.EmailField('邮箱')
    url = models.fields.URLField('网址')
    text = models.fields.TextField('评论')
    post = models.ForeignKey(Post, verbose_name='文章', on_delete=models.CASCADE)
    created_time = models.fields.DateTimeField('创建时间',auto_now_add=True)

    class Meta:
        verbose_name = '评论' #单数形式
        verbose_name_plural = verbose_name  #复数形式
        ordering = ['-created_time']
    def __str__(self):
        return '{}-{}-{}'.format(self.id, self.name, self.text[:10])