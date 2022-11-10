from django.db import models
from django.conf import settings
# Create your models here.

class Category(models.Model):
    sort = models.CharField(max_length=255)

    def __str__(self):
        return '{}'.format(self.sort)


class Product(models.Model):
    name = models.CharField(max_length=30)
    content = models.CharField(max_length=100)
    color = models.TextField()
    price = models.TextField()
    size = models.TextField()
    hits = models.PositiveIntegerField(default=0, verbose_name="조회수")
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_restaurants')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_category')


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    product_image = models.URLField(max_length = 200)

