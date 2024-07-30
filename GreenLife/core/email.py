from django.core.mail import send_mail
from django.conf import settings


def send_welcome_email(user_email):
    subject = 'Welcome to GreenLife'
    message = ("Thanks for signing up. This is a test. \n"
               "If you are seeing this, it worked. Please do not respond.")
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user_email]

    send_mail(subject, message, from_email, to_email)


def send_subscription_email(user_email):
    subject = 'Thank you for subscribing!'
    message = ("Thank you for subscribing. \n"
               "We are grateful to you for patronizing our service.")
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user_email]
    send_mail(subject, message, from_email, to_email)


def send_cancellation_email(user_email):
    subject = 'Your cancellation has been confirmed.'
    message = ("Cherished user, \n"
               "We are writing to confirm that you have successfully cancelled your subscription.")
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user_email]
    send_mail(subject, message, from_email, to_email)


def send_complaint_email(user_email):
    subject = 'Your complaint has been received.'
    message = ("Cherished customer, \n"
               "Your complaint has been received and we are working hard to resolve it. \n"
               "A representative has been assigned your case and will reach out to you soon.\n"
               "Thank you for reaching out.")
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user_email]
    send_mail(subject, message, from_email, to_email)