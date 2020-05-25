"""
修改desc字段在admin的form表单中的显示为多行输入(类似于textfield),
而不是单行,
"""
# from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from dal import autocomplete

from blog.models import Category, Tag, Post


class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea(attrs={'rows': 4,}),
                           label='摘要',
                           required=False,)
    # 一对多
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=autocomplete.ModelSelect2(url='category-autocomplete'),
        label='分类',
    )
    # tag 是多对多标签
    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='tag-autocomplete'),
        label='标签',
    )

    content = forms.CharField(
        widget=CKEditorUploadingWidget(),
        label='正文',
        required=True
    )

    class Meta:
        model = Post
        fields = ('category', 'tag', 'title', 'desc', 'content', 'status')
