from django.contrib.auth.models import User
from django.db import models
from django.utils.functional import cached_property


class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS  = (
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
        (STATUS_NORMAL,'正常'),
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
    attached_file = models.CharField(max_length=2048, blank=True, verbose_name='附件')


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
            postlist = tag.post_set.filter(status=Post.STATUS_NORMAL)\
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
            postlist = category.post_set.filter(status=Post.STATUS_NORMAL)\
                .select_related('owner').prefetch_related('tag')
        return postlist, category

    @classmethod
    def hot_posts(cls):
        """ 获取最热文章排名, 根据访问量 """
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')[:5]

    @classmethod
    def latest_posts(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-created_time')[:5]

    @classmethod
    def get_all(cls):
        return  cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-created_time')

    @cached_property
    def tags(self):
        return ','.join(self.tag.values_list('name', flat=True))


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


