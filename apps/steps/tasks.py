from django.shortcuts import get_object_or_404

from project.celery import app


@app.task
def check_steps_from_screenshot(step_id):
    from apps.steps.models import Step

    steps = get_object_or_404(Step, id=step_id)
    print(steps.amount_matches_screenshot(steps.steps, str(steps.photo)))
