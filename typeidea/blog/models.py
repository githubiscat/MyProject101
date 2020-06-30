import os

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count, Sum, Q
from django.utils.functional import cached_property
from django.utils.html import format_html

from typeidea.settings.base import MEDIA_ROOT


class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=50, verbose_name='名称')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS,
                                         verbose_name='状态')
    is_nav = models.BooleanField(default=False, verbose_name='是否为导航')
    owner = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    @classmethod
    def get_navs(cls):
        """ 获得所有为导航的分类"""
        categories = cls.objects.filter(status=cls.STATUS_NORMAL)
        nav_categories = []
        normal_categories = []
        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_categories.append(cate)
        return {
            'navs': nav_categories,
            'categorys': normal_categories,
        }

    class Meta:
        verbose_name = verbose_name_plural = '分类'


class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=10, verbose_name='名称')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS,
                                         verbose_name='状态')
    owner = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    @classmethod
    def get_all(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '标签'


class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )

    category = models.ForeignKey(Category, on_delete=models.PROTECT,
                                 verbose_name='分类')
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    title = models.CharField(max_length=255, verbose_name='标题')
    desc = models.CharField(max_length=1024, blank=True, verbose_name='摘要')
    content = models.TextField(verbose_name='正文', help_text='正文为MarkDown')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS,
                                         verbose_name='状态')
    owner = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    pv = models.PositiveIntegerField(default=1, verbose_name='访问量')
    uv = models.PositiveIntegerField(default=1, verbose_name='访客量')
    attached_file = models.CharField(max_length=2048, blank=True,
                                     verbose_name='附件')
    title_image = models.ImageField(upload_to='title_image',
                                    verbose_name='标题图片',
                                    default='title_image.png',
                                    blank=True)
    is_top = models.BooleanField(default=False, verbose_name='是否置顶',
                                 choices=((True, '置顶'), (False, '不置顶')))
    top_carousel_image = models.ImageField(upload_to='carousel_iamge',
                                           verbose_name='置顶轮播图',
                                           blank=True)

    def title_image_data(self):
        return format_html(
            '<img src="{}" style="width:200px; height:150px;"/>'.format(
                self.title_image.url)
        )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id']  # 根据文章ID降序排列

    # 因为文章的页面无非是根据 tag category来过滤显示的 所以可以单独拿出写在Model层
    # 需要过滤时直接调用函数即可
    @staticmethod
    def get_by_tag(tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag = None
            postlist = []
        else:
            postlist = tag.post_set.filter(status=Post.STATUS_NORMAL) \
                .select_related('owner', 'category')
        return postlist, tag

    @staticmethod
    def get_by_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
            postlist = []
        else:
            postlist = category.post_set.filter(status=Post.STATUS_NORMAL) \
                .select_related('owner').prefetch_related('tag')
        return postlist, category

    @classmethod
    def hot_posts(cls):
        """ 获取最热文章排名, 根据访问量 """
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')[:5]

    @classmethod
    def latest_posts(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by(
            '-created_time')[:5]

    @classmethod
    def get_all(cls):

        return cls.objects.select_related('owner', 'category').filter(status=cls.STATUS_NORMAL).order_by(
            '-created_time')

    @classmethod
    def get_top(cls):
        return cls.objects.filter(is_top=True).order_by('created_time')

    @cached_property
    def tags(self):
        return ','.join(self.tag.values_list('name', flat=True))

    @property
    def get_next_post(self):
        return Post.objects.values('id', 'title'). \
            filter(status=Post.STATUS_NORMAL). \
            filter(id__lt=self.id).order_by('id').last()

    @property
    def get_last_post(self):
        return Post.objects.values('id', 'title'). \
            filter(status=Post.STATUS_NORMAL). \
            filter(id__gt=self.id).order_by('id').first()

    @property
    def get_normal_comment(self):
        return self.comment_set.filter(status=1)  # Comment中status=1代表已经激活

    @property
    def comment_count(self):
        """计算评论数量
        本来想在模板中计算，但是因为评论和回复是两张表，计算总量时比较麻烦
        所以使用了cc这个orm查询，这样一次db查询就可以统计出数量！ 但不确定查询速度如何！
        """
        cc = self.comment_set.all().annotate(
            r_count_1=Count('reply__status', filter=Q(reply__status=1)),
            r_count_2=Count('reply__status',
                            filter=Q(reply__status=2))).aggregate(
            r_sum_1=Sum('r_count_1'),
            r_sum_2=Sum('r_count_2'),
            c_sum_1=Count('status', filter=Q(status=1)),
            c_sum_2=Count('status', filter=Q(status=2)),
        )
        for k, v in cc.items():
            if v is None:
                cc[k] = 0
        c_normal_count = cc['c_sum_1'] + cc['r_sum_1']  # 审核过可以显示的总的数量
        c_review_count = cc['c_sum_2'] + cc['r_sum_2']  # 待审核的数量
        return [c_normal_count, c_review_count]


class PostUploadFile(models.Model):
    STATUS_USED = 1
    STATUS_UNUSED = 0
    STATUS_ITEMS = (
        (STATUS_USED, '使用中'),
        (STATUS_UNUSED, '未使用'),
    )
    cookie_stamp = models.CharField(max_length=128, verbose_name='编辑文章时的标识')
    file_path = models.CharField(max_length=1028,
                                 verbose_name='上传文件路径',
                                 blank=True)
    status = models.PositiveSmallIntegerField(default=STATUS_UNUSED,
                                              choices=STATUS_ITEMS,
                                              verbose_name='引用状态')
    post = models.PositiveIntegerField(verbose_name='所属文章', null=True)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def how_long_time(self):
        """查看数据对象已经创建了多长时间"""
        pass
