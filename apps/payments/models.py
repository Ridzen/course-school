from django.db import models
from apps.payments.choices import MONTH, SUBSCRIPTION, PACKAGE
from apps.masterclass.models import MasterClass
from apps.course.models import Course
from django.contrib.auth import get_user_model
User = get_user_model()


class CourseMembership(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='memberships',
        verbose_name='Курс'
    )
    membership_type = models.PositiveSmallIntegerField(
        choices=SUBSCRIPTION, default=MONTH, verbose_name='Тип подписки'
    )
    price = models.DecimalField(
        default=0, verbose_name='Цена',
        max_digits=9, decimal_places=2
    )

    def __str__(self):
        return f'Курс: {self.course}, Тип подписки: {self.get_membership_type_display()}'

    class Meta:
        verbose_name = 'Пакет курса'
        verbose_name_plural = 'Пакеты курсов'


class UserMembership(models.Model):
    user = models.OneToOneField(
        User, related_name='user_membership', verbose_name='Пользователь',
        on_delete=models.CASCADE
    )
    course_membership = models.ForeignKey(
        CourseMembership,
        on_delete=models.SET_NULL, null=True, verbose_name='Подписка на курс', blank=True
    )
    register_request = models.OneToOneField(
        'RegisterRequest', on_delete=models.PROTECT, verbose_name='Форма заявки',
        null=True, blank=True, related_name='rg_membership'
    )
    active = models.BooleanField(
        default=False, verbose_name='Активный?'
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата подписки'
    )

    def __str__(self):
        if self.course_membership:
            return f'Студент: {self.user.email}, Тип подписки на курс: \
                {self.course_membership.get_membership_type_display()}'
        return f'Студент: {self.user.email}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Package(models.Model):
    title = models.CharField(
        verbose_name='Заголовок/Тип Оплаты', max_length=255
    )
    description = models.TextField(
        'Описание/Состав пакета'
    )
    price = models.DecimalField(
        default=0, verbose_name='Цена',
        max_digits=9, decimal_places=2
    )
    type = models.PositiveSmallIntegerField(
        choices=PACKAGE, default=MONTH, verbose_name='Тип пакета'
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='Создан'
    )

    def __str__(self):
        return f'Пакет: {self.get_type_display()}, Описание:{self.title}'

    class Meta:
        verbose_name = 'Пакет'
        verbose_name_plural = 'Пакеты'


class RegisterRequest(models.Model):
    class SUBSCRIPTION_STATUS(models.TextChoices):
        USED = 'used', 'used',
        EXPIRED = 'expired', 'expired'
    full_name = models.CharField(max_length=200, verbose_name='ФИО')
    phone = models.CharField(max_length=50, verbose_name='Номер телефона')
    email = models.EmailField(
        max_length=200, verbose_name='Почта', unique=True)
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата заявки'
    )
    package_membership = models.ForeignKey(
        Package, on_delete=models.PROTECT, verbose_name='Пакет')
    payment_url = models.URLField(
        verbose_name='Ссылка оплаты', blank=True, null=True)
    payment_id = models.CharField(
        verbose_name='ID оплаты', blank=True, null=True, max_length=255)
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено?")

    # membership fields
    type = models.CharField(
        verbose_name='Тип пакета', null=True, blank=True, max_length=255,
    )
    paid_price = models.CharField(
        verbose_name='Конечная сумма', max_length=255, null=True, blank=True)
    status = models.CharField(
        max_length=32,
        verbose_name='Статус подписки',
        choices=SUBSCRIPTION_STATUS.choices,
        default=SUBSCRIPTION_STATUS.USED,
    )
    # fill after payment
    expire_date = models.DateField(
        verbose_name='Срок истечения', null=True, blank=True)
    paid_date = models.DateField(
        verbose_name='Дата покупки', null=True, blank=True)

    def __str__(self):
        return f'Заявка на подписку: {self.email}'

    class Meta:
        verbose_name = 'Заявка на регистрацию'
        verbose_name_plural = 'Заявки на регистрации'

    def save(self, *args, **kwargs):
        if not self.type:
            self.type = self.package_membership.get_type_display()
        super().save(*args, **kwargs)


class CoursePackage(models.Model):
    package = models.ForeignKey(
        Package, on_delete=models.CASCADE, verbose_name='Пакет', related_name='base_compound'
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name='Курс',
    )

    def __str__(self):
        return f'{self.id}, Курс: {self.course.title}'


class MasterClassPackage(models.Model):
    package = models.ForeignKey(
        Package, on_delete=models.CASCADE, verbose_name='Пакет',
    )
    masterclass = models.ForeignKey(
        MasterClass, on_delete=models.CASCADE, verbose_name='Мастер-Класс',
    )

    def __str__(self):
        return f'{self.id}, Мастер-Класс: {self.masterclass.title}'


class RegisterRequestPayment(models.Model):
    register_request = models.ForeignKey(
        RegisterRequest, on_delete=models.CASCADE, verbose_name='Заявка на регистрацию', related_name='rg_payments'
    )
    paid_date = models.DateField(
        verbose_name='Дата покупки', null=True, blank=True)
    expire_date = models.DateField(
        verbose_name='Срок истечения', null=True, blank=True)
    type = models.CharField(max_length=255, verbose_name='Тип пакета/Описание')
    paid_price = models.CharField(
        verbose_name='Конечная сумма', max_length=255, null=True, blank=True)
    is_paid = models.BooleanField(default=False, verbose_name='Оплачено')

    def __str__(self):
        return f'paid object: {self.id}'

    class Meta:
        verbose_name = 'Оплата пользователя'
        verbose_name_plural = 'Оплаты пользователей'

