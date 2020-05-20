"""
避免富文本编辑器因为异步上传文件所产生的垃圾文件, 这个文件会根据数据库记录的已上传文件de信息与
提交表单之后的post.content字段内容做对比, 在每次创建或更新Post时, 都会检查是否上传或删除了文件
并检测这些文件有没有被使用,根据不同状态做出不同的操作
"""
import os

from blog.models import PostUploadFile
from typeidea.settings.base import BASE_DIR


class CleanJunkFile:
    def __init__(self, cookie_stamp, src_list, old_src_list, post_id):
        self.cookie_stamp = cookie_stamp
        self.src_list = src_list
        self.old_src_list = old_src_list
        self.post_id = post_id

    def clean_file(self):
        unused_file_dict = self.getjunkfile_and_setfileinfo(self.cookie_stamp,
                                                            self.src_list,
                                                            self.post_id)
        for file_path, f_obj in unused_file_dict.items():
            print('删除的文件:', file_path)
            self.delete_file(file_path, f_obj)

        del_old_file_list = self.getjunkfile_on_oldpost(self.src_list,
                                                        self.old_src_list)
        self.delete_old_file(del_old_file_list)
        print('本次提交删除的旧的文件列表:', del_old_file_list)

    @staticmethod
    def getjunkfile_and_setfileinfo(cookie_stamp, src_list, post_id):
        """
        只作用于当创建或更新post内容时上传一个新的文件的情况,
        当更新post内容时想删除旧的image或其他文件,这个方法并不适用
        """
        unuse_file_dict = {}
        files = PostUploadFile.objects.filter(cookie_stamp=cookie_stamp)
        for file in files:
            if file.file_path in src_list:
                file.status = 1  # 1代表这个文件已经被使用
                file.post = post_id  # 设置文件引用
                file.save()
            else:
                unuse_file_dict[file.file_path] = file
                # 文件在POST提交后并没有使用,所以我们需要删除这条记录

        return unuse_file_dict

    @staticmethod
    def getjunkfile_on_oldpost(src_list, old_src_list):
        """
        处理更新post内容时editor删除以前提交的文件所形成的垃圾文件.
        背景: 虽然我们在ckeditor编辑器内删除了文件,但是删除的只是html img标签及其引用,
        真正的文件在服务器中并没有删除.
        """
        # post_obj = Post.objects.get(id=post_id)
        need_del_src = []
        for i in old_src_list:
            # 如果旧的文件不在新提交的文件列表中的话 则认为这个文件需要删除
            if i not in src_list:
                need_del_src.append(i)
        return need_del_src

    @staticmethod
    def delete_file(file_path, db_file_obj):
        file_path = os.path.join(BASE_DIR, file_path.strip('/'))
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)  # 删除垃圾文件
                db_file_obj.delete()  # 删除数据库中的文件记录
            except Exception as e:
                print('ERROR {}'.format(e))
        else:
            print('{} 文件不存在'.format(file_path))

    @staticmethod
    def delete_old_file(file_path_list):
        # 删除旧的文件的同时还需要删除数据库文件上传表
        # 避免产生大量数据库查询,所以使用的in
        old_file_obj = PostUploadFile.objects.filter(file_path__in=file_path_list)
        for old_file in old_file_obj:
            old_file_path = os.path.join(BASE_DIR,
                                         old_file.file_path.strip('/'))
            if os.path.isfile(old_file_path):
                try:
                    os.remove(old_file_path)  # 删除文件
                    old_file.delete()  # 删除数据库上的文件记录
                except:
                    print('ERROR: {}删除失败, 数据ID{}'.format(old_file_path, old_file.id))
            else:
                print('ERROR {}不是一个文件, 数据库ID{}'.format(old_file_path, old_file.id))