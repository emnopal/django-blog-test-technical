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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from user_auth import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('register', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('profile', user_views.profile, name='profile'),
    path('accounts/profile/', user_views.profile, name='profile'),
    path('accounts/profile', user_views.profile, name='profile'),
    path('accounts/profile/<int:user_id>/', user_views.ProfileDetailView.as_view(), name='account_detail'),
    path('profile/<int:user_id>/', user_views.ProfileDetailView.as_view(), name='account_detail'),
    path('login/', auth_views.LoginView.as_view(template_name="user_auth/login.html"), name='login'),
    path('login', auth_views.LoginView.as_view(template_name="user_auth/login.html"), name='login'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name="user_auth/login.html"), name='login'),
    path('accounts/login', auth_views.LoginView.as_view(template_name="user_auth/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="user_auth/logout.html"), name='logout'),
    path('logout', auth_views.LogoutView.as_view(template_name="user_auth/logout.html"), name='logout'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name="user_auth/logout.html"), name='logout'),
    path('accounts/logout', auth_views.LogoutView.as_view(template_name="user_auth/logout.html"), name='logout'),
    path('summernote/', include('django_summernote.urls')),
    path('profile/<int:user_id>/followers/add', user_views.AddFollower.as_view(), name='add-follower'),
    path('profile/<int:user_id>/followers/remove', user_views.RemoveFollower.as_view(), name='remove-follower'),
    path('', include('django_blog.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
