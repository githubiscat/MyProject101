import re
content = """
<div class="post_content"><p><img alt="" src="/media/article_images/root/2020/05/20/747d7ee3.jpg" style="height:500px; width:500px" /></p>

<p><img alt="" src="/media/article_images/root/2020/05/20/youke.jpg" style="height:300px; width:300px" /></p>

<p><a href="/media/article_images/root/2020/05/20/highlightpack.js">aaa</a></p></div>
"""
MEDIA_URL = '/media/'
r_obj = re.compile(r'(?:src|href)="({m}.*?)"'.format(m=MEDIA_URL))
src_list = r_obj.findall(content)
print(src_list)


