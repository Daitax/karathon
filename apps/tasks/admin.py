import datetime

from django.contrib import admin

# Register your models here.
from apps.account.models import Participant
from apps.tasks.models import IndividualTask


class IndividualTaskAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "karathon":
            from apps.core.models import Karathon
            kwargs["queryset"] = Karathon.objects.filter(type='individual', finished_at__gte=datetime.datetime.now())
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # def save_model(self, request, obj, form, change):
    #     super().save_model(request, obj, form, change)

        # if not change:
        #     participants = Participant.objects.filter(category=obj.category, karathon=obj.karathon)
        #     bulk_data = []
        #     for participant in participants:
        #         data = IndividualTaskParticipant(
        #             participant=participant,
        #             task=obj,
        #             is_completed=False
        #         )
        #         bulk_data.append(data)
        #
        #     IndividualTaskParticipant.objects.bulk_create(bulk_data)


admin.site.register(IndividualTask, IndividualTaskAdmin)
