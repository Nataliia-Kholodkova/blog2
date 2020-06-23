"""CodeBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path


from . import views

app_name = 'api'

urlpatterns = [
    path('users/register', views.UserCreateView.as_view(), name='create_user'),
    path('users/login', views.UserLoginView.as_view(), name='login_user'),
    path('posts/', views.PostListView.as_view(), name='posts'),
    path('posts/create', views.PostCreateView.as_view(), name='create_post'),
    path('posts/<pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/<pk>/comments', views.CommentPostView.as_view(), name='post_comments'),
    path('comment/add', views.CommentCreateView.as_view(), name='add_comment'),
    path('comment/<pk>', views.CommentDetailView.as_view(), name='comment_detail'),
    path('comment/delete/<pk>', views.CommentDeletelView.as_view(), name='delete_comment'),
    path('comment/update/<int:pk>', views.CommentUpdateView.as_view(), name='edit_comment'),
    path('posts/update/<pk>', views.PostUpdateView.as_view(), name='update_post'),
    path('posts/delete/<pk>', views.PostDeletelView.as_view(), name='delete_post'),

    # path('search', views.Search.as_view(), name='search'),
]

