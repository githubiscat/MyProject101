from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from blog.models import Category


class BlogTestCase(TestCase):
    def test_query_speed(self):
        user = User.objects.all().filter()
        Category.objects.bulk_create([
            Category(name='Testcase_category%s' % i, owner=user)
            for i in range(10000)
        ])
