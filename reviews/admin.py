from django.contrib import admin

# Register your models here.
from .models import Review, Comment

# Register your models here.
admin.site.register(Review)
admin.site.register(Comment)
