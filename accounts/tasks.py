from celery import shared_task
from django.core.mail import send_mail
from decouple import config


@shared_task
def send_confirmation_mail(user, code):
    send_mail(
        subject='Письмо активации | ',
        message='Чтобы активировать аккаунт нужно ввести данный код:'
        f'\n\n{code}\n'
        f'\nНикому не передавайте данный код!'
        '\n\n\n',
        from_email=config('EMAIL_USER'),
        recipient_list=[user],
        fail_silently=False,
    )


@shared_task
def send_password_reset_mail(user, code):
    send_mail(
        subject='Письмо для сброса пароля | ',
        message='Чтобы приступить к процессу сброса пароля нужно ввести данный код:'
                f'\n\n{code}\n'
                f'\nНикому не передавайте данный код!'
                '\n\n\n',
        from_email=config('EMAIL_USER'),
        recipient_list=[user],
        fail_silently=False,
    )

@shared_task
def password_change_notification(user):
    send_mail(
        subject='Сброс пароля | ',
        message="Ваш пароль был успешно изменен!",
        from_email=config('EMAIL_USER'),
        recipient_list=[user],
        fail_silently=False,
    )


@shared_task
def send_welcome_message(user):
    send_mail(
        subject='Поздравляем с успешной регистрацией! ',
        message="Добро пожаловать!",
        from_email=config('EMAIL_USER'),
        recipient_list=[user],
        fail_silently=False,
    )
