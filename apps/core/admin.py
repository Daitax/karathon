from django.contrib import admin

# Register your models here.
from apps.core.models import Category, Karathon, Task


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class KarathonAdmin(admin.ModelAdmin):
    list_display = ('number', 'starts_at', 'finished_at', 'type',)


class TaskAdmin(admin.ModelAdmin):
    list_display = ('date', 'category', 'karathon', 'task')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Karathon, KarathonAdmin)
admin.site.register(Task, TaskAdmin)
