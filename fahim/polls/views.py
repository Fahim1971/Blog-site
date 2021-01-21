from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect, reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .NewFroms import SignUpForm, UserProfileChange, ProfilePic
from django.views.generic import CreateView, UpdateView, ListView, DetailView, TemplateView, View, DeleteView

from .forms import CommentForm
from .models import Blog, Comment, Likes
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


class MyBlog(LoginRequiredMixin, TemplateView):
    template_name = 'my_blogs.html'

#
# def blog_list(request):
#     return render(request, 'blog_list.html', context={})


class BlogList(ListView):
    context_object_name = 'blogs'
    model = Blog
    template_name = 'blog_list.html'
    # queryset = Blog.objects.order_by('-publish_date')# - before publish_date for descending order \\\ alternative is done in model meta class


class CreateBlog(LoginRequiredMixin,
                 CreateView):  # class based view // LoginRequiredMixin is used instead of decorator in class based vieww
    model = Blog
    template_name = 'create_blog.html'
    fields = ('blog_title', 'blog_content', 'blog_image')

    def form_valid(self, form):
        blog_obj = form.save(commit=False)
        blog_obj.author = self.request.user
        title = blog_obj.blog_title
        blog_obj.slug = title.replace(" ", "-") + "-" + str(uuid.uuid4())
        blog_obj.save()
        return HttpResponseRedirect(reverse('blogList'), )


def gallery(request):
    return render(request, 'gallery.html')


# def form(request):
#     return render(request, 'form.html')


def sign_up(request):
    form = SignUpForm()
    registered = False
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            registered = True

    dict = {'form': form, 'registered': registered}

    return render(request, 'signup.html', context=dict)


def login_page(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
    return render(request, 'login.html', context={'form': form})


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


@login_required
def profile(request):
    return render(request, 'profile.html', context={})


@login_required
def user_change(request):
    current_user = request.user
    form = UserProfileChange(instance=current_user)
    if request.method == 'POST':
        form = UserProfileChange(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            form = UserProfileChange(instance=current_user)
    return render(request, 'change_profile.html', context={'form': form})


@login_required
def pass_change(request):
    current_user = request.user
    changed = False
    form = PasswordChangeForm(current_user)
    if request.method == 'POST':
        form = PasswordChangeForm(current_user, data=request.POST)
        if form.is_valid():
            form.save()
            changed = True
    return render(request, 'pass_change.html', context={'form': form, 'changed': changed})


@login_required
def add_pro_pic(request):
    form = ProfilePic()
    if request.method == 'POST':
        form = ProfilePic(request.POST, request.FILES)
        if form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.user = request.user
            user_obj.save()
            return HttpResponseRedirect(reverse('profile'))
    return render(request, 'pro_pic_add.html', context={'form': form})


@login_required
def change_pro_pic(request):
    form = ProfilePic(instance=request.user.user_profile)
    if request.method == 'POST':
        form = ProfilePic(request.POST, request.FILES, instance=request.user.user_profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile'))
    return render(request, 'pro_pic_add.html', context={'form': form})


@login_required
def blog_detail(request, slug):
    blog = Blog.objects.get(slug=slug)
    comment_form = CommentForm()
    already_liked = Likes.objects.filter(blog=blog, user=request.user)
    if already_liked:
        liked = True
    else:
        liked = False
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.save()
            return HttpResponseRedirect(reverse('blog_detail', kwargs={'slug': slug}))
    return render(request, 'blog_detail.html', context={'blog': blog, 'comment_form': comment_form, 'liked': liked})


@login_required
def liked(request, pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    already_liked = Likes.objects.filter(blog=blog, user=user)
    if not already_liked:
        liked_post = Likes(blog=blog, user=user)
        liked_post.save()
    return HttpResponseRedirect(reverse('blog_detail', kwargs={'slug': blog.slug}))


@login_required
def unliked(request, pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    already_liked = Likes.objects.filter(blog=blog, user=user)
    already_liked.delete()
    return HttpResponseRedirect(reverse('blog_detail', kwargs={'slug': blog.slug}))


class UpdateBlog(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ('blog_title', 'blog_content', 'blog_image')
    template_name = 'edit_blog.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('blog_detail', kwargs={'slug': self.object.slug})




















