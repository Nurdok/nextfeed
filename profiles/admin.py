from django.contrib import admin

from profiles.models import UserProfile, UserEntryDetail


class UserProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'next_slug')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserEntryDetail)
