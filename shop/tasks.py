from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.core.mail import get_connection

from shop.utils import generate_invoice


@shared_task
def send_invoice_mail(user_id, receiver, order_id):
    subject = f"Invoice of order #{order_id}"
    html_invoice = generate_invoice(user_id, order_id, html=True)
    with get_connection(timeout=settings.EMAIL_TIMEOUT) as connection:
        send_mail(
            subject=subject,
            message=strip_tags(html_invoice),
            from_email=settings.EMAIL_HOST_USER,
            html_message=html_invoice,
            recipient_list=[receiver],
            connection=connection,
            fail_silently=False,
        )
    return "Successfully Sent"
