from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from datetime import datetime, timedelta, timezone

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

    @property
    def joined_string(self):
        time = datetime.now(tz=timezone.utc) - self.date_joined

        if time < timedelta(minutes=1):
            return '방금'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.date_joined.date()
            return str(time.days) + '일'
        else:
            return False