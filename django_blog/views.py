import datetime
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import connection

from user_auth.models import Profile
from .models import Post
from django_summernote.widgets import SummernoteInplaceWidget, SummernoteWidget
from .forms import CommentForm
from django.shortcuts import render, get_object_or_404


class PostListView(LoginRequiredMixin, ListView):
    template_name = "django_blog/post_list.html"
    context_object_name = 'post_list'
    paginate_by = 5

    def get_queryset(self):
        profile = Profile.objects.get(user_id=self.request.user)
        user = profile.user
        list_following_username = [user]
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    p.user_id user
                FROM user_auth_profile p
                JOIN user_auth_profile_followers pf ON p.id = pf.profile_id
                JOIN auth_user a on p.user_id = a.id
                WHERE pf.user_id = %s
            """, [self.request.user.id])
            row = cursor.fetchone()
            if row:
                for r in row:
                    following_profile = Profile.objects.get(user_id=r)
                    list_following_username.append(following_profile.user)

        posts = Post.objects.filter(author__in=list_following_username).order_by('-created_on')
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_login = get_object_or_404(Profile, user_id=self.request.user)
        context['user_login'] = user_login
        return context

def post_list_view_redirect(request):
    return redirect('post_list')

def post_detail(request, pk):
    template_name = "django_blog/post_detail.html"
    post = get_object_or_404(Post, pk=pk)
    user_login = get_object_or_404(Profile, user_id=request.user)
    comments = post.comments.filter(post_id=pk)
    new_comment = None  # Comment posted
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        new_comment = comment_form.save(commit=False)
        new_comment.post = post
        new_comment.save()
        return redirect('post_detail', pk=pk)
    else:
        comment_form = CommentForm()
    values = {"post": post, "comments": comments, "new_comment": new_comment, "comment_form": comment_form, "user_login": user_login}
    return render(request, template_name, values)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content", "status"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super(PostCreateView, self).get_form(form_class)
        form.fields["content"].widget = SummernoteWidget()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_login = get_object_or_404(Profile, user_id=self.request.user)
        context['user_login'] = user_login
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "content", "status"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.updated_on = datetime.datetime.now()
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_form(self, form_class=None):
        form = super(PostUpdateView, self).get_form(form_class)
        form.fields["content"].widget = SummernoteWidget()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_login = get_object_or_404(Profile, user_id=self.request.user)
        context['user_login'] = user_login
        return context


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_login = get_object_or_404(Profile, user_id=self.request.user)
        context['user_login'] = user_login
        return context


def about(request):
    return render(request, "django_blog/about.html", {"title": "About"})
