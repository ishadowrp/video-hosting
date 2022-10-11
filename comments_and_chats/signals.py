from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from .models import PrivatChat, CommentRating, Comment
from accounts.models import Notification, ProfileData
from media_storage.models import MediaRating
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from accounts.nexmo import request_verification


@receiver(post_save, sender=PrivatChat)
def notify_users_new_private_message(sender, instance, created, **kwargs):
    if created:
        for user in instance.chat_users:
            if user != instance.author:
                notification = Notification.objects.create(user=user,
                                                           message=f'You have received a new message from {str(instance.author)}',
                                                           status_read=False)
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)('notification_%s' % instance.media.author.username, {
                    "type": "chat.message",
                    "room_id": instance.media.author.username,
                    "username": str(instance.author),
                    "message": {
                        'notification_id': notification.pk,
                        'username': str(notification.user),
                        'userID': str(notification.user.pk),
                        'created': str(notification.created),
                        'message': notification.message,
                        'status': notification.status_read
                        }
                })


@receiver(post_save, sender=MediaRating)
def notify_users_new_rating(sender, instance, created, **kwargs):
    if created and not (instance.media.author == instance.author):
        notification = Notification.objects.create(user=instance.media.author,
                                                   message=f'You have received a new rating on your media from {str(instance.author)}',
                                                   status_read=False)
        channel_layer = get_channel_layer()
        print(channel_layer)
        print('notification_%s' % instance.media.author.username)
        async_to_sync(channel_layer.group_send)('notification_%s' % instance.media.author.username, {
            "type": "chat.message",
            "room_id": instance.media.author.username,
            "username": str(instance.author),
            "message": {
                'notification_id': notification.pk,
                'message': notification.message,
                'status': notification.status_read
            }
        })


@receiver(post_save, sender=Comment)
def notify_users_new_rating(sender, instance, created, **kwargs):
    if created and not (instance.media.author == instance.author):
        notification = Notification.objects.create(user=instance.media.author,
                                                   message=f'You have received a new comment on your media from {str(instance.author)}',
                                                   status_read=False)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)('notification_%s' % instance.media.author.username, {
            "type": "chat.message",
            "room_id": instance.media.author.username,
            "username": str(instance.author),
            "message": {
                'notification_id': notification.pk,
                'message': notification.message,
                'status': notification.status_read
            }
        })


@receiver(post_save, sender=CommentRating)
def notify_users_new_comment_rating(sender, instance, created, **kwargs):
    if created and not (instance.comment.author == instance.author):
        notification = Notification.objects.create(user=instance.comment.author,
                                                   message=f'You have received a new rating on your comment from {str(instance.author)}',
                                                   status_read=False)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)('notification_%s' % instance.comment.author.username, {
            "type": "chat.message",
            "room_id": instance.comment.author.username,
            "username": str(instance.author),
            "message": {
                'notification_id': notification.pk,
                'message': notification.message,
                'status': notification.status_read
            }
        })


@receiver(post_save, sender=ProfileData)
def send_verification(sender, instance, created, **kwargs):
    if created:
        request_verification(instance)
