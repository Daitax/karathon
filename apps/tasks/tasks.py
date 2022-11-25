def is_individual_task_completed(report):
    task = report.participant.today_task()
    from apps.steps.models import Step

    match task.type:
        case "walk_steps":
            if task.steps == report.steps:
                return True

        case "double_best":
            karathon = report.participant.get_active_karathon()

            best_steps = Step.objects.filter(
                participant=report.participant,
                date__gte=karathon.starts_at,
                date__lte=karathon.finished_at
            ).exclude(date=report.date).order_by('-steps').first()

            if report.steps == (best_steps.steps * 2) or report.steps == task.steps:
                return True

        case "double_result_day":
            day_steps = Step.objects.get(participant=report.participant, date=task.task_date_report)

            if report.steps == (day_steps.steps * 2):
                return True

        case "improve_best":
            karathon = report.participant.get_active_karathon()

            best_steps = Step.objects.filter(
                participant=report.participant,
                date__gte=karathon.starts_at,
                date__lte=karathon.finished_at
            ).exclude(date=report.date).order_by('-steps').first()

            if report.steps > best_steps.steps or report.steps == task.steps:
                return True

        case "improve_result_day":
            day_steps = Step.objects.get(participant=report.participant, date=task.task_date_report)

            if report.steps > day_steps.steps * 2:
                return True

        case "add_steps_to_day":
            day_steps = Step.objects.get(participant=report.participant, date=task.task_date_report)

            if report.steps == day_steps.steps + task.steps:
                return True

        case "palindrome":
            copy_report_steps = report.steps
            result_number = 0

            while copy_report_steps != 0:
                digit = copy_report_steps % 10
                result_number = result_number * 10 + digit
                copy_report_steps = int(copy_report_steps / 10)

            if result_number == report.steps:
                return True

        case "steps_of_consecutive_digits":
            digit_list = sorted([int(a) for a in str(report.steps)])
            for i in range(len(digit_list) - 1):
                if digit_list[i] + 1 == digit_list[i + 1]:
                    pass
                else:
                    return False
            return True

        case "steps_multiple_number":
            if report.steps % task.multiple_number == 0:
                return True

        case "add_steps_to_report_digit":
            day_steps = Step.objects.get(participant=report.participant, date=task.task_date_report)
            digit_list = [int(a) for a in str(day_steps.steps)]
            steps = int(digit_list[task.position - 1]) * 1000

            if report.steps == steps:
                return True

        case "best_personal_record":
            best_steps = Step.objects.filter(
                participant=report.participant
            ).exclude(date=report.date).order_by('-steps').first()

            if report.steps > best_steps.steps or report.steps == task.steps:
                return True

    return False
