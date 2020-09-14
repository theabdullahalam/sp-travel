from django.urls import path
from . import views
 
urlpatterns = [
 
    path('', views.index, name='index'),
 
    path('post/<slug:slug>', views.post, name='post'),
    path('post/<slug:slug>/', views.post, name='post'),

    path('posts/<str:section>/', views.posts, name='posts'),
    path('posts/<str:section>', views.posts, name='posts'),
    path('posts/<str:section>/<slug:slug>', views.posts, name='posts'),
    path('posts/<str:section>/<slug:slug>/', views.posts, name='posts'),
    path('posts/<str:section>/<slug:slug>/page/<int:pageno>', views.posts, name='posts'),
    path('posts/<str:section>/<slug:slug>/page/<int:pageno>/', views.posts, name='posts'),

    path('places', views.places, name='places'),
    path('places/', views.places, name='places'),
    path('places/page/<int:pageno>', views.places, name='places'),
    path('places/page/<int:pageno>/', views.places, name='places'),

    path('about', views.about, name='about'),
    path('about/', views.about, name='about'),
 
]