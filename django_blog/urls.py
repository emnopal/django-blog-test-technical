from django.urls import path, re_path

from . import views
from .views import (
    PostDetailView,
    PostListView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    PostListViewRedirect
)

urlpatterns = [

    # frontend route
    path('', PostListView.as_view(), name='post_list'),
    re_path(r'^post/?$', PostListViewRedirect.as_view(), name='post_list_redirect'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('about/', views.about, name='about_page'),

    # backend route
]
