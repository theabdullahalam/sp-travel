from django.urls import path
from . import views
 
urlpatterns = [
 
    path('', views.index, name='index'),
 
    path('post/<slug:slug>', views.post, name='post'),
    path('posts/<str:category>', views.posts, name='posts'),
    path('posts/<str:category>/', views.posts, name='posts'),
    path('posts/<str:category>/page/<int:pageno>', views.posts, name='posts'),

    path('about', views.about, name='about'),
    path('about/', views.about, name='about'),
 
]