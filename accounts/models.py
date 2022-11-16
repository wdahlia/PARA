from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class User(AbstractUser):
    followings = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers"
    )
    profile_image = ProcessedImageField(
        upload_to="images/",
        blank=True,
        null=True,
        processors=[ResizeToFill(200, 200)],
        format="JPEG",
        options={"quality": 80},
    )
    content = models.CharField(max_length=50)
