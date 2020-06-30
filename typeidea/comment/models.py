from django.db import models

from blog.models import Post


class Comment(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ACTIVE = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '已审核'),
        (STATUS_DELETE, '删除'),
        (STATUS_ACTIVE, '待审核'),
    )

    target = models.ForeignKey(Post, on_delete=models.PROTECT,
                               verbose_name='评论目标')
    content = models.CharField(max_length=2000, verbose_name='内容')
    nickname = models.CharField(max_length=32, verbose_name='昵称')
    website = models.URLField(verbose_name='网站', blank=True)
    email = models.EmailField(verbose_name='邮箱')
    phone = models.CharField(max_length=11, verbose_name='电话',default='')
    ip = models.CharField(max_length=16, verbose_name='IP地址', blank=True)
    active_code = models.CharField(max_length=32, verbose_name='激活码', blank=True)
    status = models.PositiveIntegerField(default=STATUS_ACTIVE,
                                         choices=STATUS_ITEMS,
                                         verbose_name='状态')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    @classmethod
    def get_all(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL)\
            .select_related('target').order_by('-created_time')

    @classmethod
    def get_latest(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL)\
            .select_related('target').order_by('-created_time')[:5]

    @property
    def get_normal_reply(self):
        return self.reply_set.filter(status=1)  # 在Reply中status=1代表回复已经审核

    def __str__(self):
        return 'C_id' + str(self.id)

    class Meta:
        verbose_name = verbose_name_plural = '评论'


class Reply(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ACTIVE = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '已审核'),
        (STATUS_DELETE, '删除'),
        (STATUS_ACTIVE, '待审核'),
    )
    REPLY_COMMENT = 0
    REPLY_REPLY = 1
    REPLY_ITEMS = (
        (REPLY_COMMENT, '对评论回复'),
        (REPLY_REPLY, '对回复回复')
    )
    status = models.PositiveSmallIntegerField(default=STATUS_ACTIVE,
                                              choices=STATUS_ITEMS,
                                              verbose_name='状态')
    comment = models.ForeignKey(Comment, on_delete=models.PROTECT,
                                   verbose_name='目标评论ID')
    reply_id = models.PositiveIntegerField(verbose_name='目标回复ID')
    reply_type = models.PositiveSmallIntegerField(default=REPLY_COMMENT,
                                                  choices=REPLY_ITEMS,
                                                  verbose_name='回复类型')
    from_name = models.CharField(max_length=32, verbose_name='回复人昵称')
    from_email = models.EmailField(verbose_name='回复人邮箱')
    from_website = models.URLField(verbose_name='回复人站点', blank=True)
    phone = models.CharField(max_length=11, verbose_name='电话', blank=True)
    ip = models.CharField(max_length=16, verbose_name='IP地址', blank=True)
    active_code = models.CharField(max_length=32, verbose_name='激活码',
                                   blank=True)
    to_name = models.CharField(max_length=32, verbose_name='被回复人昵称')
    from_content = models.CharField(max_length=1024, verbose_name='回复内容')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    @classmethod
    def get_reply_by_commnent(cls, c_id):
        return cls.objects.filter(status=cls.STATUS_NORMAL).\
            filter(comment_id=c_id).order_by('created_time')
    @classmethod
    def get_reply_by_id(cls, r_id):
        return cls.objects.get(id=r_id)

    def get_reply_target_content(self):
        if self.reply_type == 0:
            return None
        else:
            return self.get_reply_by_id(self.reply_id)
    class Meta:
        verbose_name = verbose_name_plural = '回复'


class Feedback(models.Model):
    email = models.EmailField(max_length=64,verbose_name='邮箱')
    phone= models.CharField(max_length=11, verbose_name='手机号码')
    content = models.CharField(max_length=1024, verbose_name='反馈内容')
    ip = models.CharField(max_length=32, verbose_name='IP地址')
    class Meta:
        verbose_name = verbose_name_plural = '意见反馈'