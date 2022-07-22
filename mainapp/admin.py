from django.contrib import admin
from mainapp.models import Resources, Quota, User


@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Resources)
class ResourcesModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'user')
    search_fields = ('title', 'user')


@admin.register(Quota)
class QuotaModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'limit')
    search_fields = ('limit', 'user')
