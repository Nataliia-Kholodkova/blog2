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

app_name = 'news'

urlpatterns = [
    path('', views.ArticlesList.as_view(), name='home'),
    path('posts/', views.PostList.as_view(), name='posts'),
    path('posts/filter', views.PostFilterView.as_view(), name='post_filter'),
    path('search', views.Search.as_view(), name='search'),
    path('create', views.AddPost.as_view(), name='create_post'),
    path('<slug>', views.PostDetail.as_view(), name='post_detail'),
    path('<slug>/comment/add', views.AddComment.as_view(), name='add_comment'),
    path('<slug>/comment/<int:parent>/', views.AddComment.as_view(), name='add_comment'),
    path('<slug>/update', views.EditPost.as_view(), name='update_post'),
    path('<slug>/delete', views.DeletePost.as_view(), name='delete_post'),
    path('<slug>/comment/<int:pk>/delete/', views.DeleteComment.as_view(), name='delete_comment'),
    path('<slug>/comment/<int:pk>/update/', views.EditComment.as_view(), name='edit_comment'),
    path('search', views.Search.as_view(), name='search'),
]

