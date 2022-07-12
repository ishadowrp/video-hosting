from django.db import models
from accounts.models import CustomUser


# Create your models here.
class Media(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    media = models.FileField(upload_to='content/%Y/%m/%d/')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    views_count = models.IntegerField()

    def __str__(self):
        return f'{self.title} by {self.author} at {self.date_posted}'


class MediaRating(models.Model):
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    rating = models.IntegerField()
