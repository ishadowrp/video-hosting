from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from .models import PrivatChat, CommentRating
from accounts.models import Notification
from media_storage.models import MediaRating
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=PrivatChat)
def notify_users_new_message(sender, instance, created, **kwargs):
    if created:
        for user in instance.chat_users:
            if user != instance.author:
                notification = Notification.objects.create(user=user,
                                                           message=f'You have received a new message from {str(instance.author)}',
                                                           status_read=False)
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(user.username, {
                    'notification_id': notification.pk,
                    'username': str(notification.user),
                    'userID': str(notification.user.pk),
                    'created': notification.created,
                    'message': notification.message,
                    'status': notification.status_read
                })


@receiver(post_save, sender=MediaRating)
def notify_users_new_message(sender, instance, created, **kwargs):
    if created:
        notification = Notification.objects.create(user=instance.media.author,
                                                   message=f'You have received a new rating on your media from {str(instance.author)}',
                                                   status_read=False)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(instance.media.author.username, {
            'notification_id': notification.pk,
            'username': str(notification.user),
            'userID': str(notification.user.pk),
            'created': notification.created,
            'message': notification.message,
            'status': notification.status_read
        })


@receiver(post_save, sender=CommentRating)
def notify_users_new_message(sender, instance, created, **kwargs):
    if created:
        notification = Notification.objects.create(user=instance.comment.author,
                                                   message=f'You have received a new rating on your comment from {str(instance.author)}',
                                                   status_read=False)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(instance.comment.author.username, {
            'notification_id': notification.pk,
            'username': str(notification.user),
            'userID': str(notification.user.pk),
            'created': notification.created,
            'message': notification.message,
            'status': notification.status_read
        })
