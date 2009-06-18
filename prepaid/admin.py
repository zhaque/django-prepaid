from django.contrib import admin

from models import UnitPack

class UnitPackAdmin(admin.ModelAdmin):
    list_display = ('user', 'quantity', 'expires', 'timestamp',
                    'initial_quantity', 'is_valid')
    ordering = ('-timestamp',)
    date_hierarchy = 'timestamp'
    list_filter = ('user',)
admin.site.register(UnitPack, UnitPackAdmin)
