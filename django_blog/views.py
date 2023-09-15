import datetime
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from user_auth.models import Profile
from .models import Post
from django_summernote.widgets import SummernoteInplaceWidget, SummernoteWidget
from .forms import CommentForm
from django.shortcuts import render, get_object_or_404

# Create your views here.
# this is for render the views

class PostListView(LoginRequiredMixin, ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'django_blog/post_list.html'
    paginate_by = 5

    # def get(self, request, *args, **kwargs):
    #     test = Profile.objects.filter(user_id=request.user)
    #     test2 = Post.objects.filter(status=1).order_by('-created_on')
    #     print(test)
    #     print(test2)
    #     context = {
    #         'post': test2,
    #     }
    #     return render(request, 'django_blog/post_list.html', context)

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'django_blog/post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'author', 'status']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super(PostCreateView, self).get_form(form_class)
        print(form.fields['content'].widget)
        form.fields['content'].widget = SummernoteWidget()
        return form

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'author', 'status']

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
        form.fields['content'].widget = SummernoteWidget()
        return form

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'django_blog/about.html', {'title': 'About'})

def post_detail(request, pk):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(active=True)
    new_comment = None    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})
