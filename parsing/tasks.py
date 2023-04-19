from celery import shared_task
from django.core.mail import send_mail
from decouple import config


@shared_task
def send_call_to_admins(users: list, number, text, tg_user):
    send_mail(
        subject='Новый запрос на звонок',
        message=f'Пользователь {tg_user} оставил заявку на звонок, нужно связаться'
        f' по номеру "{number}".\n\nСообщение:\n'
        f"{text}"
        f'\n\nПосле того как свяжетесь, не забудьте отметить в админской панели',
        from_email=config('EMAIL_USER'),
        recipient_list=users,
        fail_silently=False,
    )


@shared_task
def send_conf_email_telegram(user, code):
    send_mail(
        subject='Письмо привязки телеграм аккаунта',
        message='Чтобы привязать аккаунт нужно ввести данный код:'
                f'\n\n{code}\n'
                f'\nНикому не передавайте данный код!'
                '\n\n\n',
        from_email=config('EMAIL_USER'),
        recipient_list=[user],
        fail_silently=False,
    )
