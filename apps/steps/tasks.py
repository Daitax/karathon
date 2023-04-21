from django.shortcuts import get_object_or_404

from project.celery import app


@app.task
def check_steps_from_screenshot(step_id):
    from apps.notifications.models import Notification
    from apps.steps.models import Step

    steps = get_object_or_404(Step, id=step_id)
    if not steps.amount_matches_screenshot(steps.steps, str(steps.photo))[0]:
        with open(
            "/home/sites/karathon/apps/steps/static/steps/checking_convertation.txt",
            "a+",
        ) as checking_file:
            screenshot_steps = steps.amount_matches_screenshot(
                steps.steps, str(steps.photo)
            )[1]
            checking_file.write(
                "внёс пользователь {} || "
                "считано со скриншота {} || "
                "фото {}"
                "\n------------------------------------------ \n".format(
                    steps.steps, screenshot_steps, steps.photo
                )
            )
    print(steps.amount_matches_screenshot(steps.steps, str(steps.photo)))
    Notification.success_message(steps.participant)
