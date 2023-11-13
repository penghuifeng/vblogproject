from django.urls import path
from blog import post_views

urlpatterns = [
    path('list/', post_views.post_list),
    path('add/', post_views.post_add),
    path('edit/<int:id>/', post_views.post_edit),
    path('delete/<int:id>/', post_views.post_delete)
]