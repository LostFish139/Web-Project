from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Category, Tag
from .forms import PostForm

def index(request):
    posts = Post.objects.all()
    return render(request, 'blog/index.html', {'posts': posts})
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.increase_views()  # 增加阅读量
    return render(request, 'blog/detail.html', {'post': post})
def category_posts(request, pk):
    category = get_object_or_404(Category, pk=pk)
    posts = Post.objects.filter(category=category)
    return render(request, 'blog/index.html', {'posts': posts})


def tag_posts(request, pk):
    """标签下的文章"""
    tag = get_object_or_404(Tag, pk=pk)
    posts = Post.objects.filter(tags=tag)
    return render(request, 'blog/index.html', {'posts': posts})


@login_required
def post_create(request):
    """创建新文章"""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # 设置当前用户为作者
            post.save()
            form.save_m2m()  # 保存多对多关系（标签）
            messages.success(request, '文章发布成功！')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/post_form.html', {'form': form})


@login_required
def post_update(request, pk):
    """更新文章"""
    post = get_object_or_404(Post, pk=pk)

    # 检查是否是文章作者
    if post.author != request.user:
        messages.error(request, '您没有权限编辑此文章！')
        return redirect('post_detail', pk=post.pk)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, '文章更新成功！')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_form.html', {'form': form})


@login_required
def post_delete(request, pk):
    """删除文章"""
    post = get_object_or_404(Post, pk=pk)

    # 检查是否是文章作者
    if post.author != request.user:
        messages.error(request, '您没有权限删除此文章！')
        return redirect('post_detail', pk=post.pk)

    if request.method == 'POST':
        post.delete()
        messages.success(request, '文章删除成功！')
        return redirect('index')

    return render(request, 'blog/post_confirm_delete.html', {'post': post})