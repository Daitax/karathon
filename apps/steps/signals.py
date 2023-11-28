from apps.tasks.tasks import is_task_completed
from .tasks import check_steps_from_screenshot


def check_task_complete(sender, instance, created, **kwargs):
    if created:
        from apps.steps.models import Step

        if is_task_completed(instance):
            bonus = instance.participant.today_task().bonus
            Step.objects.filter(id=instance.id).update(
                is_completed=True, bonus=bonus
            )



def check_screenshot(sender, instance, created, *args, **kwargs):
    if created:
        check_steps_from_screenshot.delay(instance.id)
