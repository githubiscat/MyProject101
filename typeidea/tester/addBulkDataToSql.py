import os
import sys
import time

from django.db import connection
from django.db.models import Count, Q, Sum

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# NOTE : the path to the Django site module "e.g pkapps"
# Must be in environment variable PYTHONPATH
if "DJANGO_SETTINGS_MODULE" not in os.environ:
    print('start')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "typeidea.settings.develop")

    import django

    django.setup()
    print('no issue')

from django.contrib.auth.models import User
from blog.models import Category, Post
from comment.models import Comment, Reply

# 获取某个文章的所有评论和回复数量

a = time.time()
post = Post.objects.get(id=17)
qs2 = post.get_normal_comment.annotate(
    r_count=Count('reply__status', filter=Q(reply__status=1))).aggregate(
    r_sum=Sum('r_count'), c_count=Count('id'))
qs3 = post.comment_set.all().annotate(
    r_count=Count('reply__status', filter=Q(reply__status=2))).aggregate(
    r_sum=Sum('r_count'), c_count=Count('id', filter=Q(status=2)))

qs = post.comment_set.all().annotate(
    r_count_1=Count('reply__status', filter=Q(reply__status=1)),
    r_count_2=Count('reply__status', filter=Q(reply__status=2))).aggregate(
    r_sum_1=Sum('r_count_1'), r_sum_2=Sum('r_count_2'),
    c_sum_1=Count('status', filter=Q(status=1)),
    c_sum_2=Count('status', filter=Q(status=2)),
)

print(qs)


print('qs2', qs2)
print('qs3', qs3)
print(time.time()-a)
