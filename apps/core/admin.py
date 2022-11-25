from django.contrib import admin

# Register your models here.
from apps.core.models import Category, CharityCategory, Karathon


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class CharityCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class KarathonAdmin(admin.ModelAdmin):
    list_display = ('number', 'starts_at', 'finished_at', 'type',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(CharityCategory, CharityCategoryAdmin)
admin.site.register(Karathon, KarathonAdmin)
