from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def get_ip_address(request):
    http_x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    remote_addr = request.META.get('REMOTE_ADDR')

    if http_x_forwarded_for:
        ip_address = http_x_forwarded_for.split(',')[-1].strip()
    elif remote_addr:
        ip_address = remote_addr
    else:
        ip_address = None

    return ip_address


def get_user_agent(request):
    http_user_agent = request.META.get('HTTP_USER_AGENT')

    if http_user_agent:
        user_agent = http_user_agent
    else:
        user_agent = None

    return user_agent


def send_reset_password_email(user):
    from_email = settings.EMAIL_FROM

    context = {
        'username': user.username,
        'site_name': settings.SITE_NAME,
        'site_url': settings.SITE_URL,
        'uid': urlsafe_base64_encode(force_bytes(user.id)).decode(),
        'token': default_token_generator.make_token(user),
    }

    subject = loader.render_to_string(
        'registration/email/password_reset_subject.txt', context)
    subject = ''.join(subject.splitlines())
    body = loader.render_to_string(
        'registration/email/password_reset_email.html', context)

    email_message = EmailMultiAlternatives(
        subject, body, from_email, [user.email])
    email_message.send()


def send_password_changed_email(user):
    from_email = settings.EMAIL_FROM

    context = {
        'username': user.username,
        'site_name': settings.SITE_NAME,
        'site_url': settings.SITE_URL,
    }

    subject = loader.render_to_string(
        'registration/email/password_changed_subject.txt', context)
    subject = ''.join(subject.splitlines())
    body = loader.render_to_string(
        'registration/email/password_changed_email.html', context)

    email_message = EmailMultiAlternatives(
        subject, body, from_email, [user.email])
    email_message.send()
