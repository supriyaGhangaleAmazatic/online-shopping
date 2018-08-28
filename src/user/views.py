"""
    User App Views
"""

from django.conf import settings
from rest_framework.exceptions import ParseError
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
import sendgrid
import random
from sendgrid.helpers.mail import Email, Content, Mail
from .models import User, ResetPassword
from .permissions import UserAccessPermission
from .serializers import UserLoginSerializer, UserSerializer, RequestResetPasswordSerializer, ValidateResetPasswordSerializer, ResetPasswordSerializer

from datetime import datetime, timedelta


class UserViewSet(ModelViewSet):
    """
        User Model Viewset
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [UserAccessPermission]

    @action(detail=False, methods=['post'])
    def auth(self, request):
        """
             Authentication API (login)
        """
        data = request.data
        user_login_serializer = UserLoginSerializer(data=data)
        if user_login_serializer.is_valid(raise_exception=True):
            return Response(user_login_serializer.data)

    @action(detail=False, methods=['post'], url_path='reset-password')
    def request_reset_password(self, request):
        """
            Request Reset Password API
        """
        serializer = RequestResetPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(email=serializer.data['email'])
            now = datetime.now()
            possible_otp_time = now - timedelta(minutes=5)
            reset_password = ResetPassword.objects.filter(
                user_id=user.id, is_validated=False, is_reset=False, created_at__gte=possible_otp_time).first()
            if reset_password:
                otp = reset_password.otp
            else:
                while True:
                    otp = random.randint(111111, 999999)
                    otp_exists = ResetPassword.objects.filter(
                        otp=otp, is_validated=True).first()
                    if otp_exists is None:
                        break
                ResetPassword.objects.create(
                    user=user, otp=otp)
            sendgrid_inst = sendgrid.SendGridAPIClient(
                apikey=settings.SENDGRID_API_KEY)
            from_email = Email(settings.DEFAULT_FROM_MAIL)
            to_email = Email(serializer.data['email'])
            subject = "Amazatic Dummy E-commerce Site Reset password"
            content = Content(
                "text/plain", "Hello, Please use following OTP for resetting your password.\n\t %s" % otp)
            mail = Mail(from_email, subject, to_email, content)
            mail_response = sendgrid_inst.client.mail.send.post(
                request_body=mail.get())
            if not mail_response.status_code in [200, 202]:
                raise ParseError(detail='Not able to send email.')
            response_serializer = RequestResetPasswordSerializer(
                data={'message': 'OTP has been sent to your registered Email address', 'email': serializer.data['email']})
            if response_serializer.is_valid(raise_exception=True):
                return Response(response_serializer.data, status=HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='reset-password/validate')
    def validate_reset_password(self, request):
        validate_serializer = ValidateResetPasswordSerializer(
            data=request.POST)
        if validate_serializer.is_valid(raise_exception=True):
            return Response({'message': 'Data validated successfully.'}, status=HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='reset-password/reset')
    def reset_password(self, request):
        reset_serializer = ResetPasswordSerializer(data=request.POST)
        if reset_serializer.is_valid(raise_exception=True):
            user = User.objects.get(email=reset_serializer.data['email'])
            user.set_password(reset_serializer.data['password'])
            user.save()
            ResetPassword.objects.filter(
                id=reset_serializer.data['reset_password_id']).update(is_reset=True)
            return Response({'message': 'Password Reset successfull.'}, status-HTTP_200_OK)
