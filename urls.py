from django.urls import path
from . import views
from .views import  Add_Post, DetailArticleView, LikeView, Delete, search
from django.contrib.auth import views as auth_views


app_name='blog'
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('detail/<int:pk>/', DetailArticleView.as_view(), name='post_detail'),
    # path('detail/<int:pk>/', views.post_detail, name= 'post_detail'),
    path('add_post/',Add_Post.as_view(), name='add_post' ),
    # path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('like/<int:pk>/', LikeView, name='like_post'),
    path('detail/<int:pk>/delete/', Delete.as_view(), name= 'Delete'),
    path('signup/', views.signup, name='signup'),
    # path('search/', views.search, name=search)
    path('search/', views.search, name='search')
    ]