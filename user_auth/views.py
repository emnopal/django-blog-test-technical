from multiprocessing import context
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.db import connection

from django_blog.models import Post
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Hi {username}! Your account has been created! Now login!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user_auth/register.html', {'form': form})


class CurrentProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'user_auth/profile.html'

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user_id=request.user)
        user = profile.user
        posts = Post.objects.filter(author=user).order_by('-created_on')

        paginator = Paginator(posts, 5)
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)

        followers = profile.followers.all()
        is_following = False
        for follower in followers:
            if follower == request.user:
                is_following = True
                break
            else:
                is_following = False
        number_of_followers = len(followers)

        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, f'Your account has been updated!')
                return redirect('profile')

        else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.profile)

        context = {
            'u_form': u_form,
            'p_form': p_form,
            'user_login': request,
            'post_list': posts,
            'is_following': is_following,
            'number_of_followers': number_of_followers,
            'paginator': paginator,
            'is_paginated': True,
        }
        return render(request, 'user_auth/profile.html', context)

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'user_auth/user_profile.html'

    def get(self, request, user_id, *args, **kwargs):
        profile = Profile.objects.get(user_id=user_id)
        user = profile.user
        posts = Post.objects.filter(author=user, status=1).order_by('-created_on')

        paginator = Paginator(posts, 5)
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)

        followers = profile.followers.all()
        is_following = False
        for follower in followers:
            if follower == request.user:
                is_following = True
                break
            else:
                is_following = False
        number_of_followers = len(followers)

        context = {
            'user': user,
            'profile': profile,
            'user_login': request,
            'post_list': posts,
            'is_following': is_following,
            'number_of_followers': number_of_followers,
            'paginator': paginator,
            'is_paginated': True,
        }
        return render(request, 'user_auth/user_profile.html', context)

class AddFollower(LoginRequiredMixin, View):
    def post(self, request, user_id, *args, **kwargs):
        profile = Profile.objects.get(user_id=user_id)
        profile.followers.add(request.user)
        return redirect('account_detail', user_id=user_id)

class RemoveFollower(LoginRequiredMixin, View):
    def post(self, request, user_id, *args, **kwargs):
        profile = Profile.objects.get(user_id=user_id)
        profile.followers.remove(request.user)
        return redirect('account_detail', user_id=user_id)


# @login_required
# def follow_user(request, username):
#     user_to_follow = User.objects.get(username=username)
#     request.user.following.add(Follower(following=user_to_follow))
#     return redirect('account_detail', user_id=user_to_follow.id)

# @login_required
# def unfollow_user(request, username):
#     user_to_unfollow = User.objects.get(username=username)

#     follower_instance = Follower.objects.filter(following=user_to_unfollow).first()

#     if follower_instance:
#         follower_instance.delete()

#     return redirect('account_detail', user_id=user_to_unfollow.id)
