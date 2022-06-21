from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from reply.forms import ReplyForm
from reply.models import Reply


@login_required(login_url='/user/login')
def create(request):
    if request.method == "GET":
        replyForm = ReplyForm()
        return render(request, 'reply/create.html', {'replyForm': replyForm})
    elif request.method == "POST":
        replyForm = ReplyForm(request.POST)
        if replyForm.is_valid():
            reply = replyForm.save(commit=False)
            reply.writer = request.user
            reply.save()
        return redirect('/reply/read/' + str(reply.id))


def list(request):
    replys = Reply.objects.all().order_by('-id')

    return render(request, 'reply/list.html', {'replys':replys})


def read(request, rid):
    reply = Reply.objects.get(id=rid)

    return render(request, 'reply/read.html', {'reply':reply})


@login_required(login_url='/user/login')
def delete(request, rid):
    reply = Reply.objects.get(id=rid)
    if request.user != reply.writer:
        return redirect('/reply/list')
    reply.delete()

    return redirect('/reply/list')


@login_required(login_url='/user/login')
def update(request, rid):
    reply = Reply.objects.get(id=rid)
    if request.method == "GET":
        replyForm = ReplyForm(instance=reply)
        return render(request, 'reply/create.html', {'replyForm': replyForm})
    elif request.method == "POST":
        replyForm = ReplyForm(request.POST, instance=reply)
        if replyForm.is_valid():
            reply = replyForm.save(commit=False)
            reply.save()
        return redirect('/reply/read/' + str(reply.id))
