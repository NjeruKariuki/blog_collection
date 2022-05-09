from django.urls import path
from .views import PostListView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, postdetail
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name="blog-home"),
    path('post/<int:pk>/', postdetail, name="post-detail"),
    #path('post/<int:pk>/', PostDetailView.as_view(), name="post-detail"),
    path('post/new', PostCreateView.as_view(), name="post-create"),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name="post-update"),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name="post-delete"),
    path('about/', views.about, name="blog-about"),
]