from django.db import models
from products.models import Product
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

# Create your models here.


class Review(models.Model):
    grade_choices = (
        ("1", "⭐"),
        ("2", "⭐⭐"),
        ("3", "⭐⭐⭐"),
        ("4", "⭐⭐⭐⭐"),
        ("5", "⭐⭐⭐⭐⭐"),
    )
    grade = models.CharField(max_length=2, choices=grade_choices)
    content = models.CharField(max_length=160)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    review_image = ProcessedImageField(
        null=True,
        upload_to="images/",
        blank=True,
        processors=[ResizeToFill(1200, 960)],
        format="JPEG",
        options={"quality": 90},
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.CharField(max_length=160)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
