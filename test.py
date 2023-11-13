import markdown

# # 1. 定义一个初始的md字符串
# body = '# 如何学好django'
#
# # 2. 调用markdown.markdown函数把md字符串转换成html字符串
# body_html = markdown.markdown(body)
#
# # 3. 输出结果：'<h1>如何学好django</h1>'
# print(body_html)


# 1. 定义一个初始的md字符串
body = '''
# 如何学好django'
我们应该跟着汤老师学
## 如何学好django1
## 如何学好django2
'''

# 2. 创建一个对象 Markdown
md = markdown.Markdown(extensions=[
  'markdown.extensions.extra',
  'markdown.extensions.codehilite',
  'markdown.extensions.toc',
])

# 3. 调用md函数把md字符串转换成html字符串
body_html = md.convert(body)

# 4. 输出结果：'<h1>如何学好django</h1>'
# print(body_html)

print(md.toc)

