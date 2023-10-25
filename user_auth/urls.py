"""
URL configuration for protergo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.urls import path, re_path
from user_auth import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [

    # frontend route
    path('register', user_views.RegisterView.as_view(), name='register'),

    path('login', auth_views.LoginView.as_view(template_name="user_auth/login.html"), name='login'),
    re_path(r'accounts/login/?$', auth_views.LoginView.as_view(template_name="user_auth/login.html"), name='login'),

    path('logout', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/logout', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    re_path(r'^accounts/profile/?$', user_views.CurrentProfileDetailView.as_view(), name='profile'),
    path('profile', user_views.CurrentProfileDetailView.as_view(), name='profile'),

    path('accounts/profile/<str:username>', user_views.ProfileDetailView.as_view(), name='account_detail'),
    path('profile/<str:username>', user_views.ProfileDetailView.as_view(), name='account_detail'),

    path('profile/<int:user_id>/followers/add', user_views.AddFollower.as_view(), name='add-follower'),
    path('profile/<int:user_id>/followers/remove', user_views.RemoveFollower.as_view(), name='remove-follower'),

    # backend route
]
