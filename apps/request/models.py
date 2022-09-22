from django.db import models

# Create your models here.


class Questionnaire(models.Model):

    """Модель анкеты"""

    full_name = models.CharField(max_length=30, unique=True, verbose_name="ФИО")
    phone_number = models.BigIntegerField(verbose_name="номер телефона")
    email = models.EmailField(verbose_name='Email')
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'questionnare_db'
        verbose_name_plural = 'Анкеты'
        verbose_name = "Анкета"

    def __str__(self):
        return self.full_name



