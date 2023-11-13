from django.urls import path
from blog import views

urlpatterns = [
    path('', views.index),
    path('posts/<int:id>/', views.detail),
    path('archives/<int:year>/<int:month>/', views.archives),
    path('categories/<int:id>/', views.categories),
    path('search/', views.search),
    path('page1/', views.page1),
    path('page2/', views.page2),
    path('form1/', views.form1),
    path('form2/', views.form2),
    path('form3/', views.form3),
]