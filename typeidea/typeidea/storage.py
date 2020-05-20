"""
为上传的图片添加水印
DJango 提供的默认存储方式是文件存储, 我们可以定制自己的存储方式,
在存储文件之前添加图片水印, 我们需要继承django.core.files.storage
"""
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile
from matplotlib import font_manager as fm

from typeidea.settings.base import IMAGE_WATERMARK_TEXT


class WatermarkStorage(FileSystemStorage):
    def save(self, name, content, max_length=None):
        # 处理逻辑
        if 'image' in content.content_type:
            # 添加水印, 水印内容在项目settings中
            image = self.watermark_with_text(content, IMAGE_WATERMARK_TEXT, 'beige')
            content = self.convert_image_to_file(image, name)
        return super().save(name, content, max_length=max_length)

    def convert_image_to_file(self, image, name):
        temp = BytesIO()
        image.save(temp, format='PNG')
        file_size = temp.tell()
        return InMemoryUploadedFile(temp, None, name, 'image/png', file_size, None)

    def watermark_with_text(self, file_obj, text, color, fontfamily=None):
        image = Image.open(file_obj).convert('RGBA')
        draw = ImageDraw.Draw(image)
        width, height = image.size
        margin_right = 20
        margin_bottom = 15

        if fontfamily:
            font = ImageFont.truetype(fontfamily, int(height/20))
        else:
            # 动态寻找字体样式文件
            font_family = fm.findfont(fm.FontProperties(family='cmtt10'))
            font = ImageFont.truetype(font_family, int(height/20))
        # text = text.encode('utf-8')
        textWidth, textHeight = draw.textsize(text, font)
        x = int(width - textWidth - margin_right)  # 计算横轴位置
        y = int(height -textHeight - margin_bottom)  # 计算纵轴位置
        draw.text((x, y), text, color, font)
        return image
