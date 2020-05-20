"""
正则提取Post模型的content字段中的包含的img file标签的src属性
目的: 知道文章的内容使用了多少media file, 避免产生垃圾文件
"""
import re

from typeidea.settings.base import MEDIA_URL


def find_all(content):
    r_obj = re.compile(r'(?:src|href)="({}.*?)"'.format(MEDIA_URL))
    src_list = r_obj.findall(content)
    return src_list