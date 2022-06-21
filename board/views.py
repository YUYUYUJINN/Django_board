import bid
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect

from board.forms import PostForm
from board.models import Post


def mainPage(request):
    return render(request, 'board/index.html')


@login_required(login_url='/user/login')
def create(request):
    if request.method == "GET":
        postForm = PostForm()
        context = {'postForm': postForm}
        return render(request, 'board/create.html', context)
    elif request.method == "POST":
        postForm = PostForm(request.POST)
        if postForm.is_valid():
            post = postForm.save(commit=False)
            post.writer = request.user
            post.save()

        return redirect('/board/readGet/'+str(post.id))


def listGet(request):
    posts = Post.objects.all().order_by('-id')

    context = {'posts': posts}

    return render(request, 'board/list.html', context)


def readGet(request, bid):
    post = Post.objects.get(Q(id=bid))
    context = {'post': post}

    return render(request, 'board/read.html', context)


@login_required(login_url='/user/login')
def deleteGet(request, bid):
    post = Post.objects.get(id=bid)
    if request.user != post.writer:
        return redirect('/board/listGet')
    post.delete()

    return redirect('/board/listGet')


@login_required(login_url='/user/login')
def update(request, bid):
    post = Post.objects.get(id=bid)
    if request.method == "GET":
        postFrom = PostForm(instance=post) # 조회한 것을 폼에 담는 작업
        context = {
            'postForm' : postFrom
        }
        return render(request, 'board/update.html', context)
    elif request.method == "POST":
        postForm = PostForm(request.POST, instance=post) # 기존 게시글 수정
        if postForm.is_valid():
            post = postForm.save(commit=False)
            post.save()
        return redirect('/board/readGet/' + str(post.id))
