from django.contrib import admin
from django.db import models
from django.forms import widgets
from django.utils import safestring

from apps.account.models import Participant
# Register your models here.
from apps.core.models import Category, CharityCategory, Karathon


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class CharityCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class LinkedSelect(widgets.Select):
    # def __init__(self, *args, **kwargs):
    #     print("______")
    #     print(self)
    #     print(args)
    #     print(kwargs)
    #     print("______")
    #
    #     super().__init__(*args, **kwargs)


    def render(self, name, value, attrs=None, *args, **kwargs):
        output = [super(LinkedSelect, self).render(name, value, attrs=attrs, *args, **kwargs)]
        model = self.choices.field.queryset.model
        karathon = self.choices.field.queryset.model.karathon

        try:
            obj = model.objects.get(id=value)
            output = "<select name={name} id={id}><option value={part_id} selected>{" \
                     "part_name}</option></select>".format(
                name=name,
                id=attrs['id'],
                part_id=obj.id,
                part_name=obj,
            )

            # print(111222)
            # print(obj)
            # print(output)
            # print(3344)
        except model.DoesNotExist:
            output="tst"
        # print(22223333)
        # print(name)
        # print(value)
        # print(attrs)
        # print(karathon.field.__dict__)
        # print(kwargs)
        # print(44445555)

        return safestring.mark_safe(u''.join(output))


class KarathonParticipantTabular(admin.TabularInline):
    model = Participant.karathon.through
    extra = 1

    # formfield_overrides = {models.ForeignKey: {'widget': LinkedSelect}}

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # args = {"test": "test"}

        # if db_field.name == "karathon":
        #     kwargs["queryset"] = Karathon.objects.filter(participant=request.user)

        # karathon_id = request.resolver_match.kwargs.get('object_id')
        # kwargs['queryset'] = Participant.objects.exclude(karathon=karathon_id)
        #     print(112233)
        #     print(self)
        # print(db_field)
        # print(request)
        # print(kwargs)
        # print(334455)
        # team_id = request.resolver_match.kwargs.get('object_id')
        # try:
        #     team = Team.objects.get(id=team_id)
        #     kwargs['queryset'] = Participant.objects.filter(karathon=team.karathon)
        # except ObjectDoesNotExist:
        #     kwargs['queryset'] = Participant.objects.none()
        # return super().formfield_for_foreignkey(db_field, request, **kwargs)


class KarathonAdmin(admin.ModelAdmin):
    list_display = ('number', 'starts_at', 'finished_at', 'type', 'is_presentation',)
    inlines = [
        KarathonParticipantTabular,
    ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(CharityCategory, CharityCategoryAdmin)
admin.site.register(Karathon, KarathonAdmin)
