""" 拆分settings.py
新建文件夹 settings, 并将settings.py拷贝至目录的base.py.
新建文件product.py,文件继承base.py,并修改开发环境的配置项
目的: 拆分思想, 在开发环境, 测试环境, 生产环境中使用不同的配置项
拆分完成后需要修改 manage.py wsgi.py两个文件的 settings module配置部分,
告诉Django去哪里找settings
"""


from .base import *  # NOQA

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gai520',
        'USER': 'root',
        'PASSWORD': os.getenv('DJANGO_SQL_PW'),
        'HOST': '127.0.0.1',
        'PORT': 3306,
    }
}

# 日志模块
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(levelname)s %(asctime)s %(module)s:'
                      '%(funcName)s:%(lineno)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/typeidea.log',
            'formatter': 'default',
            'maxBytes': 1024*1024*8,  # 8M
            'backupCount': 5,
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}

# 邮件通知
ADMINS = MANAGERS = (
    ('gai', '643177348@qq.com')
)

EMAIL_HOST = "smtp.163.com"
EMAIL_PORT = 25 # 大多都是25；若使用SSL，端口号465或587
EMAIL_HOST_USER = "gai520website@163.com" #发送邮箱
EMAIL_HOST_PASSWORD = os.getenv('MY_SMTP_PW') # 使用的是QQ的授权码，不是你的密码
EMAILE_USE_TLS = True #一定要是True，否则发不了
EMAIL_FROM = "gai520website@163.com" #邮件发送人(邮件中所显示的发送人，和EMAIL_HOST_USER同)
EMAIL_TO = ['643177348@qq.com','17610139558@163.com']

# 绑定的域名
HOST_NAME = 'http://www.gai520.com'