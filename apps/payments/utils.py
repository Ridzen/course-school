from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def send_activation_code(email, activation_code):
    context = {
        "text_detail": "Спасибо за регистрацию",
        "email": email,
        "domain": "http://localhost:8000",
        "activation_code": activation_code,
    }
    msg_html = render_to_string('email.html', context)
    message = strip_tags(msg_html)
    send_mail(
        'Активация аккаунта',
        message,
        settings.EMAIL_HOST_USER,
        [email],
        html_message=msg_html,
        fail_silently=False
    )

def mailing_for_news(emails, title, description):
    context = {
        "title": title,
        "description": description,
    }
    msg_html = render_to_string('news_mailing.html', context)
    message = strip_tags(msg_html)
    send_mail(
        'Новости',
        message,
        settings.EMAIL_HOST_USER,
        emails,
        html_message=msg_html,
        fail_silently=False
    )


def get_subscription_period(type, todays_date):

    from dateutil.relativedelta import relativedelta
    if type == 'Месяц':
        return todays_date + relativedelta(months=1)
    elif type == 'Год':
        return todays_date + relativedelta(months=12)
    elif type == 'Год+':
        return todays_date + relativedelta(months=12)
