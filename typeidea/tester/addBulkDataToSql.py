import os
import sys



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

from blog.models import Category

def AddCategory():
    print('a')
    user = User.objects.all().last()
    print('b')
    Category.objects.bulk_create([
        Category(name='Test-%s' % i, owner=user) for i in range(10000, 30000)
    ])
    print('done')

def DelCategory():
    print('开始删除')
    Category.objects.filter(name__istartswith='Test').delete()

# AddCategory()
# DelCategory()

from blog.models import PostUploadFile

# for i in range(5):
#     p = PostUploadFile(cookie_stamp='aaaaaaa', file_path=str(i))
#     p.save()
#
# p = PostUploadFile.objects
# for i in p.filter(id = 1):
#     print(1)
# print('******************8')
# f_path = p.filter(file_path__in=[str(i) for i in range(10)])
# for i in f_path:
#     print(i.file_path)
from django.db import connection
#这里执行一段复杂的查询代码
print(connection.queries[-1]['sql'])


# for i in range(5):
#     pa = p.get(file_path=str(i))
#     print(pa.file_path)
#
# from django.db import connection
# #这里执行一段复杂的查询代码
# print(connection.queries[-1]['sql'])