import mistune
from django import forms

from comment.models import Comment, Reply


class CommentForm(forms.ModelForm):
    nickname = forms.CharField(
        label='昵称',
        max_length=12,
        min_length=2,
        required=True,
        error_messages={
            'required': 'Error: 昵称是必填项',
            'max_length': '最大长度不应超过12位',
            'min_length': '最小长度不应小于2位',
        },
        widget=forms.widgets.Input(
            attrs={'class': 'form-control',  'aria-label': '昵称',
                   'placeholder': '你的昵称   *必填项'}
        ),
    )
    email = forms.EmailField(
        label='Email',
        max_length=50,
        widget=forms.widgets.EmailInput(
            attrs={'class': 'form-control',
                   'aria-label': '邮箱',
                   'placeholder': '你的个人邮箱   *必填项'}
        )
    )
    website = forms.URLField(
        label='网站',
        max_length=100,
        required=False,  # 网站在form 中可以不填
        widget=forms.widgets.URLInput(
            attrs={'class': 'form-control',
                   'aria-label': '你的个人网站',
                   'title': '友情链接你的个人网站. 没有就不填.',
                   'placeholder': '友链   *可不填'}
        )
    )
    content = forms.CharField(
        label='内容',
        max_length=1600,
        widget=forms.widgets.Textarea(
            attrs={'class': 'form-control',
                   'placeholder': '你的评论将在管理员审核通过后才可展示!  所以请朋友你提交与文章内容相关的评论, 垃圾灌水评论一律删并封IP!!!',
                   'rows': 6}
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
        max_length=12,
        required=True,
        widget=forms.widgets.Input(
            attrs={'class': 'form-control',
                   'aria-label': '昵称',
                   'placeholder': '你的昵称   *必填项'}
        ),
        error_messages={
            'max_length': '昵称最大长度不超过12位',
            'required': '昵称不能为空',
        }
    )
    from_email = forms.EmailField(
        label='Email',
        max_length=50,
        widget=forms.widgets.EmailInput(
            attrs={'class': 'form-control',
                   'aria-label': '邮箱',
                   'placeholder': '你的邮箱   *必填项'}
        )
    )
    from_website = forms.URLField(
        label='网站',
        max_length=100,
        required=False,
        widget=forms.widgets.URLInput(
            attrs={'class': 'form-control',
                   'aria-label': '你的个人网站',
                   'title': '友情链接你的个人网站. 没有就不填.',
                   'placeholder': '友链   *可不填'}
        )
    )
    from_content = forms.CharField(
        label='内容',
        max_length=1600,
        widget=forms.widgets.Textarea(
            attrs={'class': 'form-control', 'placeholder': '你的评论将在管理员审核通过后才可展示!  所以请朋友你提交与文章内容相关的评论, 垃圾灌水评论一律删并封IP!!!', 'rows': 6}
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
