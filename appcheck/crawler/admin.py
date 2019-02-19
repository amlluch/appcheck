from django.contrib import admin
from .models import TargetSite, LinkedSite

# Register your models here.

@admin.register(TargetSite)
class TargetSiteAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('url', 'port', 'timeout', 'active'),
        }),
    )
    list_display = ('url', 'port', 'timeout', 'active')

admin.site.register(LinkedSite)