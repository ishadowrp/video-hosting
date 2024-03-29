from django.contrib.auth.models import User
from django.db import models


class ProfileData(models.Model):
    username = models.ForeignKey(User, related_name='profile_owner', on_delete=models.CASCADE)
    telephone = models.CharField(max_length=20)
    telephone_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username.username


def get_name(self):
    return self.username


User.add_to_class("__str__", get_name)


class Notification(models.Model):
    user = models.ForeignKey(User, related_name='Notifications_owner', on_delete=models.CASCADE)
    status_read = models.BooleanField(default=False)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


class VerificationData(models.Model):
    profile = models.ForeignKey(ProfileData, related_name='User_profile', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    request_id = models.CharField(max_length=100)
    code = models.IntegerField()


class AvatarData(models.Model):
    username = models.ForeignKey(User, related_name='photo_owner', on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='img', max_length=254, blank=True)

    def delete(self, *args, **kwargs):
        self.avatar.delete()
        super().delete(*args, **kwargs)
