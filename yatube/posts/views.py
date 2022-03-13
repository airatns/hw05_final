from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from .forms import CommentForm, PostForm
from .models import Comment, Follow, Group, Post, User

PAGES_ON_SHEET = 10


@cache_page(20)
def index(request):
    template = 'posts/index.html'
    posts = Post.objects.all()
    paginator = Paginator(posts, PAGES_ON_SHEET)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    groups = get_object_or_404(Group, slug=slug)
    posts = groups.posts.all()
    paginator = Paginator(posts, PAGES_ON_SHEET)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': groups,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    posts = Post.objects.all().filter(author=author)
    total_posts = posts.count()
    paginator = Paginator(posts, PAGES_ON_SHEET)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    following = False
    context = {
        'page_obj': page_obj,
        'author': author,
        'following': following,
        'total_posts': total_posts,
    }
    if request.user.is_authenticated:
        if Follow.objects.filter(user=request.user, author=author).exists():
            context['following'] = True
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk=post_id)
    total_posts = Post.objects.all().filter(author=post.author).count()
    form = CommentForm(request.POST or None)
    comment = Comment.objects.all().filter(post_id=post_id)
    context = {
        'post': post,
        'total_posts': total_posts,
        'form': form,
        'comments': comment,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    template = 'posts/create_post.html'
    form = PostForm(
        request.POST or None,
        files=request.FILES or None
    )
    if not form.is_valid():
        return render(request, template, {'form': form})
    new_post = form.save(commit=False)
    new_post.author = request.user
    new_post.save()
    return redirect('posts:profile', username=request.user)


@login_required
def post_edit(request, post_id):
    template = 'posts/create_post.html'
    is_edit = True
    post = Post.objects.get(pk=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    context = {
        'post': post,
        'form': form,
        'is_edit': is_edit,
        'post_id': post_id,
    }
    if request.user != post.author:
        return redirect('posts:post_detail', post_id)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id)
    return render(request, template, context)


@login_required
def add_comment(request, post_id):
    post = Post.objects.get(pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    template = 'posts/index.html'
    posts = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(posts, PAGES_ON_SHEET)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    is_follow = True
    context = {
        'page_obj': page_obj,
        'is_follow': is_follow,
    }
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user != author:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('posts:follow_index')


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.get(user=request.user, author=author).delete()
    return redirect('posts:follow_index')
