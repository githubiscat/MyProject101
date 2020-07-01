#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# 打包本项目

from setuptools import setup, find_packages

setup(
    name='gai520_blog',
    version='0.1',
    description='Blog Systemd Base On Django',
    author='Wang Gai',
    author_email='',
    url='http://www.gai520.com',
    license='MIT',
    packages=find_packages('typeidea'),
    package_dir={'': 'typeidea'},
    package_data={'': [
        'themes/*/*/*/*/*'
    ]},
    install_requires=[
        'backcall==0.2.0',
        'certifi==2020.6.20',
        'chardet==3.0.4',
        'cPython==0.0.5',
        'cycler==0.10.0',
        'decorator==4.4.2',
        'defusedxml==0.6.0',
        'diff-match-patch==20181111',
        'Django==2.0',
        'django-autocomplete-light==3.2.10',
        'django-ckeditor==5.4.0',
        'django-crispy-forms==1.9.0',
        'django-debug-toolbar==2.2',
        'django-debug-toolbar-line-profiler==0.6.1',
        'django-formtools==2.2',
        'django-import-export==2.1.0',
        'django-js-asset==1.2.2',
        'django-redis==4.10.0',
        'django-reversion==3.0.5',
        'djdt-flamegraph==0.2.13',
        'et-xmlfile==1.0.1',
        'future==0.18.2',
        'httplib2==0.9.2',
        'idna==2.10',
        'ipython==7.9.0',
        'ipython-genutils==0.2.0',
        'jdcal==1.4.1',
        'jedi==0.17.1',
        'kiwisolver==1.1.0',
        'line-profiler==2.1.2',
        'MarkupPy==1.14',
        'matplotlib==3.0.3',
        'mistune==0.8.4',
        'mysqlclient==1.4.6',
        'numpy==1.18.4',
        'odfpy==1.4.1',
        'openpyxl==2.6.4',
        'parso==0.7.0',
        'pexpect==4.8.0',
        'pickleshare==0.7.5',
        'Pillow==5.1.0',
        'prompt-toolkit==2.0.10',
        'ptyprocess==0.6.0',
        'Pygments==2.6.1',
        'pymongo==3.10.1',
        'Pympler==0.8',
        'pyparsing==2.4.7',
        'python-dateutil==2.8.1',
        'pytz==2019.3',
        'PyYAML==5.3.1',
        'redis==3.5.3',
        'requests==2.24.0',
        'six==1.14.0',
        'sqlparse==0.3.1',
        'tablib==1.1.0',
        'traitlets==4.3.3',
        'urllib3==1.25.9',
        'wcwidth==0.2.5',
        # 'xadmin==2.0.1',
        'xlrd==1.2.0',
        'xlwt==1.3.0',
    ],
    dependency_links=[
        'https://codeload.github.com/sshwsfc/xadmin/zip/django2',
    ],
    scripts=[
        'manage.py',
    ],
    entry_points={
        'console_scripts': [
            'gai520_manage = manage:main'
        ]
    }
)
