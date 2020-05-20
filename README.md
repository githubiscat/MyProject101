# MyProject101
===========================================================
Project for learning

Auther:    Gai Wang
Email:     643177348@qq.com


+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
注意事项:
在注册的ckeditor_uploader app中,我们修改了ckeditor_uploader的部分源码
更改文件为:.virtualenvs/P_typeidea/lib/python3.5/site-packages/ckeditor_uploader/views.py 99line

添加了:
 # =======My changes Start=======
        # cookie用于关联 异步上传的文件 和 editor提交的表单,
        post_stamp_ckfile = request.COOKIES.get('post_stamp_ckfile',
            'Error in ckeditor_uploader views.py: 101line')
        # 上传文件后将文件信息记录到Post app的 PostuploadFile模型中
        try:
            from blog.models import PostUploadFile
            one_file = PostUploadFile(cookie_stamp=post_stamp_ckfile, file_path=url)
            one_file.save()
        except:
            print('Error in ckeditor_uploader views.py. form blog.modles import PostUploadFile')
        # =======My changes End=======
