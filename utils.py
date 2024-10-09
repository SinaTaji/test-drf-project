from django.core.cache import cache
from rest_framework.exceptions import ValidationError

from authentication.tasks import send_sms_task
from random import randint


# ====== create and send otp ========
def GenerateAndSendOtp(phone_number):
    cache_key = f'otp:{phone_number}'
    code = randint(00000, 99999)
    print('=' * 90)
    print(code)
    print('=' * 90)
    cache.set(cache_key, code, timeout=120)
    send_sms_task.delay(phone_number, code)
    return code


# ============================================

# ============ get and check otp ==================
def GetAndCheckOtp(request, phone_number):
    otp_code_user = request.data.get('otp_code')
    if otp_code_user is None:
        raise ValidationError('کد تایید خود را وارد کنید')
    if not otp_code_user.isdigit():
        raise ValidationError('کد تایید باید فقط شامل اعداد باشد.')

    otp_code = int(otp_code_user)
    cache_key = f'otp:{phone_number}'
    otp_in_cache = cache.get(cache_key)

    if not otp_in_cache:
        raise ValidationError('کد تایید شما منقضی شده !')
    if otp_in_cache != otp_code:
        raise ValidationError('کد تایید وارد شده صحیح نمیباشد !')
    if otp_code == otp_in_cache:
        return True
# ========================================================
