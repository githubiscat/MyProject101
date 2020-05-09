import mistune
from django import forms

from comment.models import Comment, Reply


class CommentForm(forms.ModelForm):
    nickname = forms.CharField(
        label='昵称',
        max_length=100,
        widget=forms.widgets.Input(
            attrs={'class': 'form-control',  'aria-label': '昵称'}
        )
    )
    email = forms.EmailField(
        label='Email',
        max_length=50,
        widget=forms.widgets.EmailInput(
            attrs={'class': 'form-control', 'aria-label': '邮箱'}
        )
    )
    website = forms.URLField(
        label='网站',
        max_length=100,
        widget=forms.widgets.URLInput(
            attrs={'class': 'form-control',
                   'aria-label': '你的个人网站',
                   'title': '友情链接你的个人网站. 没有就不填.'}
        )
    )
    content = forms.CharField(
        label='内容',
        max_length=1600,
        widget=forms.widgets.Textarea(
            attrs={'class': 'form-control', 'placeholder': '评论内容', 'rows': 6}
        )
    )

    def clean_content(self):
        content = self.cleaned_data.get('content', '')
        if len(content) == 0:
            raise forms.ValidationError('评论内容不能为空!')
        # content = mistune.markdown(content)
        return content

    class Meta:
        model = Comment
        fields= ['nickname', 'email', 'website', 'content']


class ReplyForm(forms.ModelForm):
    from_name = forms.CharField(
        label='昵称',
        max_length=100,
        widget=forms.widgets.Input(
            attrs={'class': 'form-control', 'aria-label': '昵称'}
        )
    )
    from_email = forms.EmailField(
        label='Email',
        max_length=50,
        widget=forms.widgets.EmailInput(
            attrs={'class': 'form-control','aria-label': '邮箱'}
        )
    )
    from_website = forms.URLField(
        label='网站',
        max_length=100,
        widget=forms.widgets.URLInput(
            attrs={'class': 'form-control',
                   'aria-label': '你的个人网站',
                   'title': '友情链接你的个人网站. 没有就不填.'}
        )
    )
    from_content = forms.CharField(
        label='内容',
        max_length=1600,
        widget=forms.widgets.Textarea(
            attrs={'class': 'form-control', 'placeholder': '回复内容', 'rows': 6}
        )
    )

    def clean_from_content(self):
        from_content = self.cleaned_data.get('from_content', '')
        if len(from_content) == 0:
            raise forms.ValidationError('评论内容不能为空!')
        # from_content = mistune.markdown(from_content)
        return from_content

    class Meta:
        model = Reply
        fields= ['from_name', 'from_email', 'from_website', 'from_content']
