from django.contrib import admin

from profiles.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'next_slug')

admin.site.register(UserProfile, UserProfileAdmin)
