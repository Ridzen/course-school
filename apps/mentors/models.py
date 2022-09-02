import jwt

from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.core import validators
from django.conf import settings
from datetime import datetime
from datetime import timedelta

from apps.mentors.manager import TeacherManager


class Teacher(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        verbose_name='Полное имя', max_length=255, help_text='Akbar Maloer', db_index=True, unique=True,
    )
    phone_number = models.CharField(
        verbose_name="Номер телефона", max_length=11, unique=True, help_text='0555055934', null=True, blank=True
    )
    email = models.EmailField(
        validators=[validators.validate_email],
        unique=True,
        blank=False
    )
    subject = models.CharField(
        verbose_name='Имя урока', max_length=25, help_text='Python'
    )
    created_at = models.DateField(
        verbose_name="Дата создания", auto_now_add=True
    )

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = TeacherManager()

    def __str__(self) -> str:
        return f'Teacher: {self.username}'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'teachers'
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):

        """
        Этот метод требуется Django для таких вещей,
        как обработка электронной почты.
        Обычно это имя и фамилия пользователя.
        Поскольку мы не храним настоящее имя пользователя,
        мы возвращаем его имя пользователя.
        """

        return self.username

    def get_short_name(self):

        """
        Этот метод требуется Django для таких вещей,
        как обработка электронной почты.
        Как правило, это будет имя пользователя.
        Поскольку мы не храним настоящее имя пользователя,
        мы возвращаем его имя пользователя.
        """
        return self.username

    def _generate_jwt_token(self):

        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')
