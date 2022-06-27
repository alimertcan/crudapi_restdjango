from celery.utils.log import get_task_logger
from celery import shared_task
from django.core.mail import send_mail
import os
logger = get_task_logger(__name__)


# @shared_task(name="selam")
# def selam():
#     print("selam")
#     return None

@shared_task(name='send_otp_mail')
def send_email_task(mail_data):
    EMAIL_HOST_USER = os.getenv('email_user')
    print(EMAIL_HOST_USER,"selam")
    EMAIL_HOST_PASSWORD = os.getenv('email_pass')
    print(EMAIL_HOST_PASSWORD,"asdasdds")
    send_mail('This is from Celery', f'{mail_data}', 'alitekin@fastmail.com',['gexer58901@kahase.com'])  # you have to change email adress which is in list
