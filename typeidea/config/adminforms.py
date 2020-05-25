from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from config.models import SideBar


class SideBarForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget(),
                              label='内容',
                              required=False)
    # status = forms.IntegerField(widget=forms.Select,
    #                             label='状态',
    #                             required=True)
    class Meta:
        model = SideBar
        fields = ('title', 'display_type', 'content', 'status', 'weight')
