from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer,CustomTokenObtainPairSerializer,PasswordChangeSerializer,ProfileSerializer,EmailVerifySerializer,ResendOTPSerializer,PasswordResetrequestSerializer,PasswordResetConfirmSerializer
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from .utils import send_verification_email,genarate_email_otp,send_password_reset_email
# Create your views here.
User=get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class=RegisterSerializer
    permission_classes=[AllowAny]

    def perform_create(self, serializer):
        user=serializer.save()
        otp=genarate_email_otp(user=user)
        send_verification_email(user=user,otp=otp)



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class=CustomTokenObtainPairSerializer
    permission_classes=[AllowAny]

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Logout successful"},
                status=status.HTTP_205_RESET_CONTENT
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class PasswordChangeView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        serializer=PasswordChangeSerializer(data=request.data,context={"request":request})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(
            serializer.validated_data['new_password']
        )
        request.user.save() 

        return Response({"detail": "Password changed successfully"},status=status.HTTP_200_OK)

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class=ProfileSerializer
    permission_classes=[IsAuthenticated]

    def get_object(self):
        return self.request.user
    

class EmailVerifyView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        serializer=EmailVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user=serializer.validated_data['user']
        email_otp = serializer.validated_data["email_otp"]

        user.is_verified = True 
        user.save(update_fields=["is_verified"])

        email_otp.delete()
        
        return Response( 
            { "message": "Email verified successfully." }, 
            status=status.HTTP_200_OK,
             )

class ResendOTPView(APIView):
    permission_classes=[AllowAny]

    def post(self,request):
        serializer=ResendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        otp=genarate_email_otp(user=user)
        send_verification_email(user=user,otp=otp)

        return Response(
            {"message": "A new OTP has been sent to your email." },
            status=status.HTTP_200_OK,
            )
    
class PasswordResetRequestView(APIView):
    permission_classes=[AllowAny]

    def post(self,request):
        serializer=PasswordResetrequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        send_password_reset_email(user)

        return Response({"message": "Password reset link has been sent to your email."},status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        serializer=PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        password=serializer.validated_data['password']
        user.set_password(password)
        user.save(update_fields=["password"])
        return Response(
            {"message": "Password has been reset successfully."},
            status=status.HTTP_200_OK,
        )