from django import forms
from django.db.models import Q

from apps.tasks.models import Task


class TaskAdminForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"

    def clean(self):
        # Получаем данные с формы
        cleaned_data = super().clean()
        category = cleaned_data['category']
        date = cleaned_data['date']
        karathon = cleaned_data['karathon']

        # Ищем задания для текущего карафона и даты
        tasks = Task.objects.filter(
            karathon=karathon,
            date=date
        )

        # Фильтруем задания без категории "все категории"
        if category.id != 1:
            tasks = tasks.filter(
                Q(category=category) | Q(category_id='1')
            )

        # При изменении исключаем текущий instance
        if self.instance.id:
            tasks = tasks.exclude(id=self.instance.id)

        # Если есть задачи кроме текущей, для этой категории - выводим ошибку
        if tasks.count() > 0:
            raise forms.ValidationError(
                {
                    'category': "На эту дату в этой категории уже есть задание",
                    'date': "На эту дату в этой категории уже есть задание",
                }
            )

        return cleaned_data
