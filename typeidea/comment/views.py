import uuid

from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse

# Create your views here.
from django.template.loader import render_to_string

from comment.forms import CommentForm, ReplyForm
from comment.models import Reply, Comment
from typeidea.settings.base import HOST_NAME


def CommentView(request):
    if request.method == 'POST':
        # 获取用户的请求IP
        if request.META.__contains__('HTTP_X_FORWARDED_FOR'):
            remote_ip = request.META.get('HTTP_X_FORWARDED_FOR')
        elif request.META.__contains__('REMOTE_ADDR'):
            remote_ip = request.META.get('REMOTE_ADDR')
        else:
            remote_ip = 'Unknow'
        comment_form = CommentForm(request.POST)
        post_id = request.POST.get('postid')
        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.target_id = int(post_id)
            instance.ip = str(remote_ip)
            uuid_str = str(uuid.uuid4())
            instance.active_code = uuid_str
            instance.save()
            succeed = True
            # 生成uuid唯一值
            active_path = '{}{}?uuid={}&mark={}&id={}'.format(HOST_NAME,
                                                                reverse('active'),
                                                                uuid_str,
                                                                'comment',
                                                                instance.id)
            refuse_path = '{}{}?uuid={}&mark={}&id={}'.format(HOST_NAME,
                                                                reverse('refuse'),
                                                                uuid_str,
                                                                'comment',
                                                                instance.id)
            setblack_path = '{}{}?uuid={}&mark={}&id={}&ip={}'.format(HOST_NAME,
                                                              reverse('setblack'),
                                                              uuid_str,
                                                              'comment',
                                                              instance.id,
                                                              remote_ip)
            access_count = cache.get(str(remote_ip))
            cont = {
                'active_path': active_path,
                'refuse_path': refuse_path,
                'setblack_path': setblack_path,
                'nickname': instance.nickname,
                'email': instance.email,
                'website': instance.website,
                'comment': instance.content,
                'ip': instance.ip,
                'access_count': access_count,
                'post': instance.target.title,
            }
            email_html_str = render_to_string('blog/email_template.html', context=cont)
            # 发送审核邮件
            send_mail(subject='待审核的评论',
                      message='',
                      from_email='gai520website@163.com',
                      recipient_list=['17610139558@163.com','643177348@qq.com'],
                      html_message=email_html_str)
            return redirect(reverse('post',kwargs={'post_id': post_id}))

        else:
            return HttpResponse(
                '提交失败, 请返回! <a href="{}">返回</a> <br> Error: {}'.format(
                    reverse('post',kwargs={'post_id': post_id}), comment_form.errors))


def reply_comment(request):
    if request.method == "POST":
        # 获取用户的访问IP
        if request.META.__contains__('HTTP_X_FORWARDED_FOR'):
            remote_ip = request.META.get('HTTP_X_FORWARDED_FOR')
        elif request.META.__contains__('REMOTE_ADDR'):
            remote_ip = request.META.get('REMOTE_ADDR')
        else:
            remote_ip = 'Unknow'
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
            instance.ip = str(remote_ip)
            uuid_str = str(uuid.uuid4())
            instance.active_code = uuid_str
            instance.save()
            succeed = True
            # 生成uuid唯一值
            active_path = '{}{}?uuid={}&mark={}&id={}'.format(HOST_NAME,
                                                              reverse('active'),
                                                              uuid_str,
                                                              'reply',
                                                              instance.id)
            refuse_path = '{}{}?uuid={}&mark={}&id={}'.format(HOST_NAME,
                                                              reverse('refuse'),
                                                              uuid_str,
                                                              'reply',
                                                              instance.id)
            setblack_path = '{}{}?uuid={}&mark={}&id={}&ip={}'.format(HOST_NAME,
                                                              reverse('setblack'),
                                                              uuid_str,
                                                              'reply',
                                                              instance.id,
                                                              remote_ip,)
            access_count = cache.get(str(remote_ip))
            cont = {
                'active_path': active_path,
                'refuse_path': refuse_path,
                'setblack_path': setblack_path,
                'nickname': instance.from_name,
                'email': instance.from_email,
                'website': instance.from_website,
                'comment': instance.from_content,
                'ip': instance.ip,
                'access_count': access_count,
                'post': instance.comment.target.title  # 查询速度会比较慢
            }
            email_html_str = render_to_string('blog/email_template.html',
                                              context=cont)
            # 发送审核邮件
            send_mail(subject='待审核的评论',
                      message='',
                      from_email='gai520website@163.com',
                      recipient_list=['17610139558@163.com',
                                      '643177348@qq.com'],
                      html_message=email_html_str)

            return redirect(reverse('post', kwargs={'post_id': post_id}))
        else:
            print(reply_form.errors)
            return HttpResponse('提交失败, 请返回! <a href="{}">返回</a><br>{}'.format(
                reverse('post', kwargs={'post_id': post_id}), reply_form.errors))
    else:
        return HttpResponse('不支持的请求方式!')

def active_comment(request):
    if request.method == 'GET':
        uuid_str = request.GET.get('uuid')
        mark = request.GET.get('mark')
        id = request.GET.get('id')
        if mark == 'comment':
            comments = Comment.objects.filter(id=id)
            if len(comments) > 0:
                comment = comments.first()
                if comment.status == 1:
                    return HttpResponse('已经激活成功! 无需重复审核!')
                postid = comment.target_id
                if comment.active_code == uuid_str:
                    comment.status = 1  # 1代表审核通过
                    comment.save()
                    return redirect(reverse('post', kwargs={'post_id': postid}))
                else:
                    return HttpResponse('信息不匹配! 激活失败')
            else:
                return HttpResponse('信息不存在! 请确定是否删除!')
        elif mark == 'reply':
            replys = Reply.objects.filter(id=id)
            if len(replys) > 0:
                reply = replys.first()
                if reply.status == 1:
                    return HttpResponse('已经激活成功! 无需重复审核!')
                postid = reply.comment.target_id
                if reply.active_code == uuid_str:
                    reply.status = 1  # 1代表已经审核通过
                    reply.save()
                    return redirect(reverse('post', kwargs={'post_id': postid}))
                else:
                    return HttpResponse('信息不匹配! 激活失败')
            else:
                return HttpResponse('信息不存在! 请确定是否删除!')
    else:
        return HttpResponse('不支持的请求方式!')


def refuse_comment(request):
    if request.method == 'GET':
        uuid_str = request.GET.get('uuid')
        mark = request.GET.get('mark')
        id = request.GET.get('id')
        if mark == 'comment':
            comments = Comment.objects.filter(id=id)
            if len(comments):
                comment = comments.first()
                postid = comment.target_id
                if comment.active_code == uuid_str:
                    comment.status = 0  # 0代表需要删除
                    comment.delete()
                    return redirect(reverse('post', kwargs={'post_id': postid}))
                else:
                    return HttpResponse('信息不匹配! 激活失败')
            else:
                return HttpResponse('信息不存在! 请确定是否删除!')

        elif mark == 'reply':
            replys = Reply.objects.filter(id=id)
            if len(replys) > 0:
                reply = replys.first()
                postid = reply.comment.target_id
                if reply.active_code == uuid_str:
                    reply.status = 0  # 0代表需要删除
                    reply.delete()
                    return redirect(reverse('post', kwargs={'post_id': postid}))
                else:
                    return HttpResponse('信息不匹配! 激活失败')
            return HttpResponse('信息不存在! 请确定是否删除!')
    else:
        return HttpResponse('不支持的请求方式!')

def set_black(request):
    if request.method == 'GET':
        uuid_str = request.GET.get('uuid')
        mark = request.GET.get('mark')
        id = request.GET.get('id')
        ip = request.GET.get('ip')
        ip_key = str(ip) + 'site_request'
        if mark == 'comment':
            comments = Comment.objects.filter(id=id)
            if len(comments):
                comment = comments.first()
                if comment.active_code == uuid_str:
                    cache.set(ip_key, 'black', 86400)
                    return HttpResponse('已将{}设为加入黑名单! 限制访问24小时!'.format(ip))
                else:
                    return HttpResponse('信息不匹配! 激活失败')
            else:
                return HttpResponse('信息不存在! 请确定是否删除!')

        elif mark == 'reply':
            replys = Reply.objects.filter(id=id)
            if len(replys) > 0:
                reply = replys.first()
                if reply.active_code == uuid_str:
                    cache.set(ip_key, 'black', 86400)
                    return HttpResponse('已将{}设为加入黑名单! 限制访问24小时!'.format(ip))
                else:
                    return HttpResponse('信息不匹配! 激活失败')
            return HttpResponse('信息不存在! 请确定是否删除!')
    else:
        return HttpResponse('不支持的请求方式!')