from django.db import models
from media_storage.models import Media
from accounts.models import CustomUser


# Create your models here.
class Comment(models.Model):
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, related_name='author', on_delete=models.CASCADE)
    media_users = models.ManyToManyField(CustomUser, related_name='media_users')
    date_posted = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return f'Written {self.author.name} at {self.date_posted}'


class CommentRating(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    rating = models.IntegerField()


class PrivatChat(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(CustomUser, related_name='owner', on_delete=models.CASCADE)
    chat_users = models.ManyToManyField(CustomUser, related_name='chat_users')
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.title
