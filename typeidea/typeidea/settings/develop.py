""" 拆分settings.py
新建文件夹 settings, 并将settings.py拷贝至目录的base.py.
新建文件devlop.py,文件继承base.py,并修改开发环境的配置项
目的: 拆分思想, 在开发环境, 测试环境, 生产环境中使用不同的配置项
拆分完成后需要修改 manage.py wsgi.py两个文件的 settings module配置部分,
告诉Django去哪里找settings
"""


from .base import *  # NOQA


DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}



