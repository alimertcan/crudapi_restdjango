from celery.utils.log import get_task_logger
from celery import shared_task
from django.core.mail import send_mail

logger = get_task_logger(__name__)


# @shared_task(name="selam")
# def selam():
#     print("selam")
#     return None

@shared_task(name='send_otp_mail')
def send_email_task(mail_data):
    send_mail('This is from Celery', f'{mail_data}', 'alitekin@fastmail.com',
              ['sabeke3183@giftcv.com'])  # you have to change email adress which is in list
