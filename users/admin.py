from django.contrib import admin
from .models import UserProfile, UserGroup, Leadership, Team
from import_export.admin import ImportExportModelAdmin

admin.site.register(UserProfile)
admin.site.register(UserGroup)
admin.site.register(Leadership)
admin.site.register(Team)


