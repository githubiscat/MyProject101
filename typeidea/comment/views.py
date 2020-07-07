import json
import os
import random
import uuid
import datetime, time

from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse

# Create your views here.
from django.template.loader import render_to_string

from blog.models import Tag, Category
from blog.tools.gen_message_api import gen_post_func
from comment.forms import CommentForm, ReplyForm, FeedbackForm
from comment.models import Reply, Comment
from config.models import SideBar
from typeidea.settings.base import HOST_NAME

def get_seconds_remaining():
    """返回当日剩余时间"""
    today = datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d')
    oneday = datetime.timedelta(days=1)  # 定义时间增量
    tomorrow = today + oneday
    now_time = datetime.datetime.today()
    seconds_remaining = (tomorrow - now_time).seconds
    return seconds_remaining

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

        # 获取验证码并验证有效性
        active_code = request.POST.get('active_code', '')
        phone = request.POST.get('phone', '')
        cache_code = cache.get(phone + 'captcha')
        if active_code != str(cache_code):
            return JsonResponse({'code': 1, 'message': '错误验证码不一致'})
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
                'phone': phone,
            }
            email_html_str = render_to_string('blog/email_template.html', context=cont)
            # 发送审核邮件
            send_mail(subject='待审核的评论',
                      message='',
                      from_email='gai520website@163.com',
                      recipient_list=['17610139558@163.com','643177348@qq.com'],
                      html_message=email_html_str)
            # return redirect(reverse('post',kwargs={'post_id': post_id}))
            return JsonResponse({'code': 0, 'message': '评论成功！ 待管理员审核通过后即可显示！'})

        else:
            # return HttpResponse(
            #     '提交失败, 请返回! <a href="{}">返回</a> <br> Error: {}'.format(
            #         reverse('post',kwargs={'post_id': post_id}), comment_form.errors))
            return JsonResponse({},status=403)
    else:
        return HttpResponse('不支持的请求方式!', status=404)


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

        # 获取验证码并验证有效性
        active_code = request.POST.get('active_code', '')
        phone = request.POST.get('phone', '')
        cache_code = cache.get(phone + 'captcha')
        if active_code != str(cache_code):
            return JsonResponse({'code': 1, 'message': '错误验证码不一致'})

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
                'post': instance.comment.target.title,  # 查询速度会比较慢
                'phone':phone,
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

            return JsonResponse({'code': 0, 'message': '评论成功！ 待管理员审核通过后即可显示！'})
        else:
            return JsonResponse({},status=403)
    else:
        return HttpResponse('不支持的请求方式!',status=404)


def feedback(request):
    """每日同一个IP只能提交一次评论"""
    # 获取访问者用户IP
    if request.META.__contains__('HTTP_X_FORWARDED_FOR'):
        remote_ip = request.META.get('HTTP_X_FORWARDED_FOR', '')
    elif request.META.__contains__('REMOTE_ADDR'):
        remote_ip = request.META.get('REMOTE_ADDR', '')
    else:
        remote_ip = ''
    ip_key = str(remote_ip) + 'feedback'
    context = {'path_mark': 'feedback'}
    if request.method == 'GET':
        navs = Category.get_navs()
        context.update(navs)
        context.update({
            'feedback_form': FeedbackForm,
        })
        if remote_ip:
            ip_value = cache.get(ip_key)
            if not ip_value:
                # 如果IP_key 没有value 认为这个IP今日没有提交feedback
                context['lock'] = 'false'
            else:
                # 有值代表今日已经提交了feedback
                context['lock'] = 'true'
                context['tip'] = '已提交成功！ 感谢你的支持！ 有了你的建议，我相信本站会越来越好！'
        else:
            return HttpResponse('ERROR， 请求失败！ 403',status=403)
        return render(request, 'blog/feedback.html', context=context)
    elif request.method == 'POST':
        navs = Category.get_navs()
        context.update(navs)
        ip_value = cache.get(ip_key)
        if ip_value:
            context.update({
                'lock': 'true',
                'tip': '你已经提交过了feedback, 感谢你的支持！'
            })
            return render(request, 'blog/feedback.html', context=context)
        else:
            feedback_form = FeedbackForm(request.POST)
            # 获取验证码并验证有效性
            active_code = request.POST.get('active_code', '')
            phone = request.POST.get('phone', '')
            cache_code = cache.get(phone + 'captcha')
            if active_code != str(cache_code):
                context.update({
                    'lock': 'true',
                    'tip': '验证码不正确！ 请检查你的手机号和验证码是否正确！'
                })
                return render(request, 'blog/feedback.html', context=context)
            if feedback_form.is_valid():
                instance = feedback_form.save(commit=False)
                instance.ip = str(remote_ip)
                instance.save()
                # 还需要短信提示！
                cont = {
                    'comment': instance.content,
                    'email': instance.email,
                    'phone': str(phone),
                    'ip': str(remote_ip),
                }
                email_html_str = render_to_string('blog/feedback_email.html',
                                                  context=cont)
                # 发送审核邮件
                send_mail(subject='收到一个新的建议',
                          message='',
                          from_email='gai520website@163.com',
                          recipient_list=['17610139558@163.com',
                                          '643177348@qq.com'],
                          html_message=email_html_str)
                expiration_time = get_seconds_remaining()
                cache.set(ip_key, 'lock', expiration_time)
                return redirect(reverse('feedback'))
            else:
                context.update({
                    'lock': 'true',
                    'tip': '提交失败！ 表单信息不正确！'
                })
                return render(request, 'blog/feedback.html', context=context)
    else:
        return HttpResponse('不支持的请求方式!',status=404)


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

def gen_active_code(request):
    """ 获取验证码的规则是：
        同一个IP每天最多3条，同一个手机号每天最多2条，短信验证码当日有效，
        验证码的刷新时间为120s.
        返回值 code: 0=发送成功，1=IP超过次数， 2=手机号超过次数,
                    3=验证码发送失败， 4=用户手机号不合法
    """
    if request.method == 'GET':
        # 获取访问者用户IP
        if request.META.__contains__('HTTP_X_FORWARDED_FOR'):
            remote_ip = request.META.get('HTTP_X_FORWARDED_FOR','')
        elif request.META.__contains__('REMOTE_ADDR'):
            remote_ip = request.META.get('REMOTE_ADDR', '')
        else:
            remote_ip = ''
        if not remote_ip:
            return JsonResponse({},status=403)

        # 从redis中获取当日IP及手机号发送次数
        phone_num = str(request.GET.get('phone_num'))
        # 简单验证手机号是否有效
        if not phone_num.isdigit() or len(phone_num)!=11 or phone_num[0]!='1':
            return JsonResponse({'code': 4, 'message': '手机号填写不正确'})


        remote_ip_key = str(remote_ip) + 'captcha'
        ip_captcha_info = cache.get(remote_ip_key)
        expiration_time = get_seconds_remaining()  # 获取有效时间
        # cache.set(remote_ip_key, ip_captcha_info, 0) ########################3
        if ip_captcha_info:
            print('a')
            ip_count = ip_captcha_info.get('ip',0)
            print(ip_count)
            # 同一ip 一天最多申请3次验证码
            if 0 < ip_count < 3:
                print('b')
                phone_count = ip_captcha_info.get(phone_num, 0)
                # 同一手机号 一天最多申请两次验证码
                if 0 < phone_count < 2:
                    print('b1')
                    ip_captcha_info[phone_num] = phone_count + 1
                elif phone_count == 0:
                    print('b2')
                    ip_captcha_info[phone_num] = 1
                else:
                    return JsonResponse({'code': 2, 'message': '同一手机号每日最多申请两次验证码，验证码当日有效！'})
                ip_captcha_info['ip'] = ip_captcha_info['ip'] + 1  # ip验证码次数加1
            else:
                print('c')
                return JsonResponse({'code': 1, 'message': '同一IP每日最多获得3次验证码，验证码当日有效！'})

        else:
            # 没有历史信息
            print('d')
            ip_captcha_info = {
                'ip': 1,
                phone_num: 1,
            }
        # 生成随机验证码
        captcha_num = ''
        for i in range(6):
            captcha_num += str(random.randint(0, 9))

        try:
            # 获得发送验证码方式
            send_msg = gen_post_func(phone_num, captcha_num)
            # 发送验证码
            cmd = os.popen(send_msg)
            return_msg = eval(cmd.read())
            cmd.close()
            send_msg_status = return_msg['Response']['SendStatusSet'][0]['Code']
        except:
            return JsonResponse({'code': 3, 'message': '短信发送失败'})
        else:
            if send_msg_status == 'Ok':
                cache.set(remote_ip_key,ip_captcha_info, expiration_time)
                phone_key = phone_num + 'captcha'
                cache.set(phone_key, captcha_num, expiration_time)
                return JsonResponse({'code':0, 'message':'短信发送成功,验证码当日有效！',})
            else:
                return JsonResponse({'code':3, 'message': '短信发送失败'})

    else:
        return HttpResponse('不支持的请求方式')
