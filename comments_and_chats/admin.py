from django.contrib import admin
from .models import Comment, CommentRating, PrivatChat

admin.site.register(Comment)
admin.site.register(CommentRating)
admin.site.register(PrivatChat)
