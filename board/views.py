from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from board.forms import PostForm
from board.models import Post
from reply.forms import ReplyForm


@login_required(login_url='/user/login')
def like(request, bid):
    post = Post.objects.get(id=bid)
    user = request.user

    if post.like.filter(id=user.id).exists():
        post.like.remove(user)
        return JsonResponse({'message': 'deleted', 'like_cnt': post.like.count()})
    else :
        post.like.add(user)  # save와 다르게 중복을 체크함
        return JsonResponse({'message' : 'added',  'like_cnt': post.like.count()})


@login_required(login_url='/user/login')
def create(request):
    if request.method == "GET":
        postForm = PostForm()  # 객체 생성, 데이터를 전달 받음
        context = {'postForm': postForm}  # 서버가 클라이언트한테 전달해주고 싶음, 딕셔너리 형태로 전달
        return render(request, 'board/create.html', context)
    elif request.method == "POST":
        postForm = PostForm(request.POST) # 객체 생성, 데이터를 전달 받음
        if postForm.is_valid():
            post = postForm.save(commit=False)  # 적용하기 전에 어떻게 저장이 되는지 확인
            post.writer = request.user  # 로그인을 한 사용자각 wirter가 되어서 작성할 수 있게 함
            post.save()

        return redirect('/board/read/'+str(post.id))


def list(request): # 리스트에 여러개의 post 객체들이 저장됨
    posts = Post.objects.all().order_by('-id')  # 데이터를 가지고 오고 싶은 모델(Post)에 데이터를 가져옴, 역순으로 정렬

    context = {'posts': posts}  # 서버가 클라이언트한테 전달해주고 싶음, 딕셔너리 형태로 전달

    return render(request, 'board/list.html', context)


def read(request, bid):

    # select_related, 정방향
    # prefetch_related, 역방향
    post = Post.objects.prefetch_related('reply_set').get(id=bid)  # reply_set이 추가로 들어감 (장고에서의 규칙임)

    replyForm = ReplyForm()
    context = {'post': post, 'replyForm': replyForm}

    return render(request, 'board/read.html', context)


@login_required(login_url='/user/login')
def delete(request, bid):
    post = Post.objects.get(id=bid)
    if request.user != post.writer:
        return redirect('/board/list')
    post.delete()

    return redirect('/board/list')


@login_required(login_url='/user/login')
def update(request, bid):
    post = Post.objects.get(id=bid)
    if request.user != post.writer:
        return redirect('/board/read/' + str(bid))

    if request.method == "GET":
        postForm = PostForm(instance=post)
        context = {'postForm': postForm}
        return render(request, 'board/create.html', context)

    elif request.method == "POST":
        postForm = PostForm(request.POST, instance=post)
        if postForm.is_valid():
            post = postForm.save(commit=False)
            post.save()
        return redirect('/board/read/' + str(bid))
