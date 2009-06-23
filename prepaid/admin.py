from django.contrib import admin

from models import UnitPack

class UnitPackAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'quantity', 'expires',
                    'initial_quantity', 'is_valid')
    exclude = ('initial_quantity',)
    ordering = ('-timestamp',)
    date_hierarchy = 'timestamp'
    list_filter = ('user',)
admin.site.register(UnitPack, UnitPackAdmin)
