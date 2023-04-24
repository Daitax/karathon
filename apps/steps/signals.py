from apps.tasks.tasks import is_individual_task_completed
from .tasks import check_steps_from_screenshot


def check_individual_task_complete(sender, instance, created, **kwargs):
    # if created:
    #     karathon = instance.participant.get_active_karathon()
    #     if karathon.type == "individual":
    #         from apps.steps.models import Step

    #         if is_individual_task_completed(instance):
    #             bonus = instance.participant.today_task().bonus
    #             Step.objects.filter(id=instance.id).update(
    #                 is_completed=True, bonus=bonus
    #             )
    #     elif karathon.type == "team":
    #         pass
    ...


def check_screenshot(sender, instance, created, *args, **kwargs):
    if created:
        check_steps_from_screenshot.delay(instance.id)
