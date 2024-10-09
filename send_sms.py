from kavenegar import *
from decouple import config


# region KaveNegar send sms ===================
def send_otp(phone_number, code):
    try:
        api = KavenegarAPI(config('KaveNegar_ApiKey'))
        params = {'sender': '1000689696',
                  'receptor': phone_number,
                  'message': f'کد تایید شما {code}'}
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)

# endregion
