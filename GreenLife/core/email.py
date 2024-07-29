from django.core.mail import send_mail
from django.conf import settings


def send_welcome_email(user_email):
    subject = 'Welcome to GreenLife'
    message = ("Thanks for signing up. This is a test. \n"
               "If you are seeing this, it worked. Please do not respond.")
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user_email]

    send_mail(subject, message, from_email, to_email)
