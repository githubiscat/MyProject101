"""
这个文件的作用是定制一个站点, 即用户管理和应用层面的管理
分为两个站点进行管理.
example:
用户管理: http://123xxx.com/superadmin/
应用管理: http://123xxx.com/admin/
除了这个文件继承AdminSite来定义自己的site外,
还需要修改urls.py admin.py中的相关配置项.
"""

from django.contrib.admin import AdminSite


class CustomSite(AdminSite):
    site_header = 'Typeidea'
    site_title = 'Typeidea 管理后台'
    index_title = '首页'


custom_site = CustomSite(name='cus_admin')