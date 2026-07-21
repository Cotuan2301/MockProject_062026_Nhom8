from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.contrib.auth.hashers import check_password

from apps.accounts.models import User
from apps.accounts.utils import generate_verification_token, mask_phone_number
from .serializers import LoginSerializer

class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"detail": "Identifier and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        identifier = serializer.validated_data.get('identifier')
        raw_password = serializer.validated_data.get('password')
        
        user = User.objects.filter(
            Q(email__iexact=identifier) | Q(phone_number=identifier)
        ).first()
        
        if not user:
            return Response(
                {"detail": "Invalid email/phone or password."},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        if not check_password(raw_password, user.password_hash):
            return Response(
                {"detail": "Invalid email/phone or password."},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        if user.status != User.Status.ACTIVE:
            return Response(
                {"detail": "Invalid email/phone or password."},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        masked_phone = mask_phone_number(user.phone_number)
        if not masked_phone:
            return Response(
                {"detail": "Invalid email/phone or password."},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        # Success (ACTIVE)
        verification_token = generate_verification_token(user.id)
        
        return Response({
            "verification_token": verification_token,
            "phone_number": masked_phone,
            "mfa_required": True
        }, status=status.HTTP_200_OK)