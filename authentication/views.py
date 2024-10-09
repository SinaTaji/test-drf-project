from django.core.cache import cache
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiParameter
from account.models import User
from .serializers import UserRegistrationSerializer
from permisions import IsAuthenticatedRedirect
from utils import GenerateAndSendOtp, GetAndCheckOtp


class RegisterView(APIView):
    """
        در این ای پی آی ما اطلاعات مورد نیاز جهت ثبت نام را از کاربر میگیریم و بررسی میکنیم و اگر درست بود بهش کد او تی پی میدیم .
    """
    permission_classes = [IsAuthenticatedRedirect]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'otp_request'
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        ser_data = self.serializer_class(data=request.data)

        if not ser_data.is_valid():
            return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
        validated_data = ser_data.validated_data

        phone_number = validated_data['phone_number']
        cache_key2 = f'register_data:{phone_number}'

        GenerateAndSendOtp(phone_number)

        cache.set(cache_key2, validated_data, timeout=300)
        request.session['user_register_key'] = {
            'phone_number': phone_number,
        }
        return Response({"message": "کد تایید شما ارسال شد"}, status=status.HTTP_200_OK)


class VerifyOTPView(APIView):
    """
    در این ای پی آی کاربر باید کد او تی پی که برای اون ارسال کردیم را وارد کنه و اگر درست بود کاربر جدید ثبت میشه و برای اون دو توکن صادر میشه که باید در هدر قرار بگیره
    """

    permission_classes = [IsAuthenticatedRedirect]

    @extend_schema(
        parameters=[
            OpenApiParameter(name='otp_code', description='کد OTP', required=True, type=str),
        ])
    def post(self, request):
        if 'user_register_key' not in request.session:
            return Response({"message": "سشن شما منقضی شده است."}, status=status.HTTP_400_BAD_REQUEST)
        phone_number = request.session['user_register_key']['phone_number']
        cache_key2 = f'register_data:{phone_number}'

        if GetAndCheckOtp(request, phone_number):
            user_data = cache.get(cache_key2)
            if not user_data:
                raise ValidationError('داده های شما منقضی شده است لطفا دوباره ثبت نام کنید')

            user_in_line = UserRegistrationSerializer(data=user_data)
            if user_in_line.is_valid():
                user_in_line.create(user_in_line.validated_data)

                user = User.objects.get(phone_number=phone_number)

                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                del request.session['user_register_key']
                cache.delete(cache_key2)
                response = Response({
                    'message': 'ثبت ‌نام با موفقیت انجام شد.'
                }, status=status.HTTP_201_CREATED)
                response['Authorization'] = f'Bearer {access_token}'
                response['X-Refresh-Token'] = str(refresh)
                return response
            return Response(user_in_line.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "کد OTP نامعتبر است."}, status=status.HTTP_400_BAD_REQUEST)


class ResendOTPView(APIView):
    """
    کاربر در حین وارد کردن و تایید کد او تی پی 2 دقیقه زمان دارد وقتی 2 دقیقه زمان به اتمام رسید با کلیک کردن روی این لینک کد دوباره ارسال میشود
    """
    permission_classes = [IsAuthenticatedRedirect]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'otp_request'

    def post(self, request):
        if 'user_register_key' not in request.session:
            return Response({"message": "سشن شما منقضی شده است."}, status=status.HTTP_400_BAD_REQUEST)
        phone_number = request.session['user_register_key']['phone_number']

        cache_key = f'otp:{phone_number}'
        otp_in_cache = cache.get(cache_key)
        if otp_in_cache:
            raise ValidationError('کد شما هنوز منقضی نشده است')

        GenerateAndSendOtp(phone_number)
        return Response('کد جدید برای شما ارسال شد', status=status.HTTP_200_OK)


class ForgotPasswordView(APIView):
    """
    وقتی کاربر با لینک فراموشی رمز عبور میاد ازش شماره میگیریم و در صورت درست بودن کد او تی پی بهش میدیم
    """

    permission_classes = [IsAuthenticatedRedirect]

    @extend_schema(
        parameters=[
            OpenApiParameter(name='phone_number', description='شماره موبایل کاربر', required=True, type=str),
        ])
    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            raise ValidationError('لطفا شماره موبایل خود را وارد کنید')
        user = User.objects.filter(phone_number=phone_number).first()
        if not user:
            raise ValidationError('کاربری با این شماره موبایل یافت نشد')

        GenerateAndSendOtp(phone_number)

        request.session['user_register_key'] = {
            'phone_number': phone_number,
        }
        return Response('کد تایید برای شما ارسال شد', status=status.HTTP_200_OK)


class ResetPasswordOtpView(APIView):
    """
    در این ای پی آی کد او تی پی که برای کاربر ارسال کردیم برای تغییر رمز را میگیریم و چک میکنیم
    """
    permission_classes = [IsAuthenticatedRedirect]

    @extend_schema(
        parameters=[
            OpenApiParameter(name='otp_code', description='کد OTP', required=True, type=str),
        ])
    def post(self, request):
        if GetAndCheckOtp(request):
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    """
    در این ای پی آی وقتی کاربر وارد شد ازش رمز عبور جدید و تکرار آن را میگیریم و اگر همه چیز درست بود رمز کاربر تغییر پیدا میکنه
    """
    permission_classes = [IsAuthenticatedRedirect]

    @extend_schema(
        parameters=[
            OpenApiParameter(name='password', description='رمز کاربر', required=True, type=str),
            OpenApiParameter(name='confirm_password', description='تکرار رمز کاربر', required=True, type=str),
        ])
    def post(self, request):
        password = request.data['password']
        password2 = request.data['password2']
        phone_number = request.session['user_register_key']['phone_number']
        if not phone_number or phone_number is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if not password or not password2:
            raise ValidationError('لطفا کلمه عبور را وارد کنید')
        if password != password2:
            raise ValidationError('کلمه عبور با تکرار آن مغایرت دارد')
        user = User.objects.get(phone_number=phone_number)
        user.set_password(password2)
        user.save()
        del request.session['user_register_key']
        return Response('رمز عبور شما تغییر کرد', status=status.HTTP_200_OK)


class LoginView(APIView):
    """
    در این ای پی آی از کاربر شماره موبایل و رمز عبور میگیریم و اگر درست بود دوتا توکن صادر میشه که باید در هدر کاربر قرار بگیره
    """
    permission_classes = [IsAuthenticatedRedirect]

    @extend_schema(
        parameters=[
            OpenApiParameter(name='phone_number', description='شماره موبایل', required=True, type=str),
            OpenApiParameter(name='password', description='رمز کاربر', required=True, type=str),
        ])
    def post(self, request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')

        if not phone_number or not password:
            return Response({'detail': 'لطفا شماره موبایل و رمز عبور را وارد کنید.'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(phone_number=phone_number).first()
        if user is None or not user.check_password(password):
            return Response({'detail': 'نام کاربری یا رمز عبور نادرست است.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    در این ای پی آی باید رفرش توکن را در بادی ارسال کنید تا در صورت صحیح بودن در لیست سیاه قرار بگیره
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        token = request.data.get('refresh')
        if not token:
            return Response({'detail': 'توکن معتبر نیست.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token_obj = OutstandingToken.objects.get(token=token)

            BlacklistedToken.objects.get_or_create(token=token_obj)

        except OutstandingToken.DoesNotExist:
            return Response({'detail': 'توکن معتبر نیست.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'detail': 'خروج با موفقیت انجام شد.'}, status=status.HTTP_205_RESET_CONTENT)
