from django.db import models
from accounts.models import CustomUser


# Create your models here.
class Media(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    media = models.FileField(upload_to='content/%Y/%m/%d/')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    views_count = models.IntegerField()


class MediaRating(models.Model):
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    rating = models.IntegerField()
