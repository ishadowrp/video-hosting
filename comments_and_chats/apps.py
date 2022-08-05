from django.apps import AppConfig


class CommentsAndChatsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'comments_and_chats'

    def ready(self):
        import comments_and_chats.signals
