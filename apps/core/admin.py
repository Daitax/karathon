from django.contrib import admin


from apps.account.models import ParticipantsKarathon
# Register your models here.
from apps.core.models import Category, CharityCategory, CustomRecordsmans, Karathon


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

    def get_queryset(self, request):
        # Специально скрываем категорию с ID = 1, что бы с админки никак с ней не взаимодействовать
        qs = super().get_queryset(request).exclude(id=1)
        return qs


class CharityCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class CustomRecordsmansAdmin(admin.ModelAdmin):
    pass

class KarathonAdmin(admin.ModelAdmin):
    list_display = ('number', 'starts_at', 'finished_at', 'type', 'is_presentation',)

class ParticipantsKarathonAdmin(admin.ModelAdmin):
    list_display = ('participant', 'karathon', 'is_active')

admin.site.register(Category, CategoryAdmin)
admin.site.register(CharityCategory, CharityCategoryAdmin)
admin.site.register(CustomRecordsmans, CustomRecordsmansAdmin)
admin.site.register(Karathon, KarathonAdmin)
admin.site.register(ParticipantsKarathon, ParticipantsKarathonAdmin)
