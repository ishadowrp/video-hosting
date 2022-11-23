from django.contrib import admin
from .models import ProfileData, Notification, VerificationData, AvatarData


class ProfileAdminUser(admin.ModelAdmin):
    list_display = ['username', 'telephone', 'telephone_verified']
    list_display_links = ('username', )
    list_filter = ('username__username', 'username__email', 'telephone_verified',)  # добавляем примитивные фильтры в нашу админку
    search_fields = ('username__username', 'username__email', 'telephone',)  # тут всё очень похоже на фильтры из запросов в базу


class NotificationAdminUser(admin.ModelAdmin):
    list_display = ['user', 'message', 'created', 'status_read']
    list_display_links = ('message', )
    list_filter = ('user__username', 'status_read', )  # добавляем примитивные фильтры в нашу админку
    search_fields = ('user__username', 'message',)  # тут всё очень похоже на фильтры из запросов в базу


class VerificationAdminUser(admin.ModelAdmin):
    list_display = ['profile', 'request_id', 'code']
    list_display_links = ('profile', )


class AvatarAdminUser(admin.ModelAdmin):
    list_display = ['username', 'avatar']
    list_display_links = ('username', )
    list_filter = ('username__username',)  # добавляем примитивные фильтры в нашу админку
    search_fields = ('username__username',)  # тут всё очень похоже на фильтры из запросов в базу


admin.site.register(ProfileData, ProfileAdminUser)
admin.site.register(Notification, NotificationAdminUser)
admin.site.register(VerificationData, VerificationAdminUser)
admin.site.register(AvatarData, AvatarAdminUser)
