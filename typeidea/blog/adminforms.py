"""
修改desc字段在admin的form表单中的显示为多行输入(类似于textfield),
而不是单行,
"""

from django import forms


class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)
