

from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse

# Create your views here.

from comment.forms import CommentForm, ReplyForm
from comment.models import Reply


def CommentView(request):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        post_id = request.POST.get('postid')
        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.target_id = int(post_id)
            instance.save()
            succeed = True
            return redirect(reverse('post',kwargs={'post_id': post_id}))

        else:
            return HttpResponse(
                '提交失败, 请返回! <a href="{}">返回</a> <br> Error: {}'.format(
                    reverse('post',kwargs={'post_id': post_id}), comment_form.errors))


def reply_comment(request):
    if request.method == "POST":
        reply_form = ReplyForm(request.POST)
        # all_value = request.POST.get_all()
        comment_id = request.POST.get('commentid')
        post_id = request.POST.get('postid')
        to_name = request.POST.get('to_name')
        reply_id = request.POST.get('reply_id')
        reply_type = request.POST.get('reply_type')
        if reply_form.is_valid():
            instance = reply_form.save(commit=False)
            instance.comment_id = int(comment_id)
            instance.to_name = to_name
            instance.reply_id = reply_id
            instance.reply_type = int(reply_type)
            instance.save()
            succeed = True
            return redirect(reverse('post', kwargs={'post_id': post_id}))
        else:
            print(reply_form.errors)
            return HttpResponse('提交失败, 请返回! <a href="{}">返回</a><br>{}'.format(
                reverse('post', kwargs={'post_id': post_id}), reply_form.errors))