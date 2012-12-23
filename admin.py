from django.contrib import admin
from models import GameTeXObject, GameTeXFieldValue

class CustomFieldInline(admin.TabularInline):
    model = GameTeXFieldValue

class GTOAdmin(admin.ModelAdmin):
    fields = ('name', 'macro', 'classes')
    readonly_fields = ('classes',)
    inlines = [CustomFieldInline]

admin.site.register(GameTeXObject, GTOAdmin)