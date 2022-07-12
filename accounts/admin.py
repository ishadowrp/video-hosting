from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'telephone']
    list_display_links = ('username', 'email',)
    list_filter = ('username', 'email',)  # добавляем примитивные фильтры в нашу админку
    search_fields = ('username', 'email', 'telephone',)  # тут всё очень похоже на фильтры из запросов в базу


admin.site.register(CustomUser, CustomUserAdmin)
