from django.urls import path
from . import views
 
urlpatterns = [
 
    path('', views.index, name='index'),
 
    path('post/<slug:slug>', views.post, name='post'),
    path('posts', views.posts, name='posts'),
    path('posts/', views.posts, name='posts'),
    path('posts/page/<int:pageno>', views.posts, name='posts'),
 
]