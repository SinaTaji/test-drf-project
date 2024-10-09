from send_sms import send_otp
from celery import shared_task


@shared_task
def send_sms_task(phone_number, code):
    """
    تسکی که پیامک را با Celery ارسال می‌کند.
    """
    send_otp(phone_number, code)
    return f"پیامک با موفقیت به {phone_number} ارسال شد."
