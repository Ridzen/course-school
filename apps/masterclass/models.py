from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.


class Category(models.Model):
    """
    Модель для темы
    """
    title = models.CharField(max_length=200, verbose_name="Название")

    class Meta:
        verbose_name = "Тема"
        verbose_name_plural = "Темы"
        ordering = ('title',)

    def __str__(self):
        return self.title


class MasterClass(models.Model):
    """
    Модель Мастер класса

    """
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, verbose_name="Тема")
    title = models.CharField(max_length=245, unique=True, verbose_name='Название')
    subtitle = models.CharField(max_length=245, unique=False, null=True, verbose_name='Под титул')
    description = models.TextField(null=True, blank=True, verbose_name='Описание мастеркласса')
    start_date = models.DateField(null=True, blank=True, verbose_name='Количество уроков')
    amount_lessons = models.CharField(max_length=200, null=True, blank=True, verbose_name="Количество уроков")
    image = models.FileField(upload_to='images/', verbose_name="Изображение", blank=True, null=True)
    video = models.URLField(verbose_name="Видео", blank=True, null=True)
    overview = models.TextField(verbose_name="Более подробное описание, мастер класса")
    duration = RichTextUploadingField(verbose_name='Продолжительность')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    in_archive = models.BooleanField(default=False, verbose_name='В архив')

    class Meta:
        verbose_name = "Мастер Класс"
        verbose_name_plural = "Мастер Классы"

    def __str__(self):
        return self.title
