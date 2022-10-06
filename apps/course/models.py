from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()


class CourseCategory(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория курса'
        verbose_name_plural = 'Категории курсов'


class Course(models.Model):
    category = models.ForeignKey(
        CourseCategory, related_name='courses', on_delete=models.CASCADE, verbose_name="Категория", null=True
    )
    title = models.CharField(max_length=200, verbose_name='Названия')
    subtitle = models.TextField(verbose_name='Подзаголовок', null=True, blank=True)
    description = models.TextField(verbose_name='Описание курса',)
    image = models.ImageField(upload_to='courses/', verbose_name='Изображение', blank=True, null=True)
    video = models.URLField(verbose_name='Видео', blank=True, null=True)
    duration_months = models.CharField(max_length=200, verbose_name='Длительность в месяцах')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ('-created',)

    def __str__(self):
        return self.title

