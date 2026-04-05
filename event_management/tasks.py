from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_registration_email_task(user_email, event_title, date, location):
    send_mail(
        subject=f"Registration for {event_title}",
        message=f"Date: {date}\nLocation: {location}",
        from_email=None,
        recipient_list=[user_email],
    )