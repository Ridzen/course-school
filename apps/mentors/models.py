import jwt

from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.core import validators
from django.conf import settings
from datetime import datetime
from datetime import timedelta
from django.utils.crypto import get_random_string


from apps.mentors.manager import CustomManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Gender(models.TextChoices):
        MALE = 'male', 'male'
        FEMALE = 'female', 'female'

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
    created_at = models.DateField(
        verbose_name="Дата создания", auto_now_add=True
    )
    fullname = models.CharField(
            max_length=250, verbose_name='ФИО', unique=True, null=True
    )
    born_date = models.DateField(
        null=True, blank=True, verbose_name='Дата рождения'
    )
    country = models.CharField(
        max_length=150, null=True, verbose_name="Страна"
    )
    city = models.CharField(
        max_length=150, verbose_name="Город", null=True, blank=True
    )
    gender = models.CharField(
            max_length=32, verbose_name='пол', choices=Gender.choices, default=Gender.MALE
    )
    avatar = models.ImageField(verbose_name='Аватар', null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomManager()

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


# class CustomUser(models.Model):
#
    # class Gender(models.TextChoices):
    #     MALE = 'male', 'male'
    #     FEMALE = 'female', 'female'

#     fullname = models.CharField(
#         max_length=250, verbose_name='ФИО', unique=True
#     )
#     born_date = models.DateField(
#         null=True, blank=True, verbose_name='Дата рождения'
#     )
#     country = models.CharField(
#         max_length=150, null=True, verbose_name="Страна"
#     )
#     email = models.EmailField(
#         verbose_name='Email', unique=True, blank=True
#     )
#     city = models.CharField(
#         max_length=150, verbose_name="Город"
#     )
#     gender = models.CharField(
#         max_length=32, verbose_name='пол', choices=Gender.choices, default=Gender.MALE
#     )
#     is_active = models.BooleanField(
#         default=False, verbose_name='Активный'
#     )
#     avatar = models.ImageField(verbose_name='Аватар')
#     activation_code = models.CharField(
#         max_length=25, blank=True, verbose_name='Код для активации'
#     )
#     objects = CustomManager()
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
#
#     def __str__(self) -> str:
#         return f"{self.email} -> {self.id}"
#
#     def create_activation_code(self):
#         code = get_random_string(
#             length=10,
#             allowed_chars='1234567890#$%!?_'
#         )
#         self.activation_code = code
#         self.save(update_fields=['activation_code'])