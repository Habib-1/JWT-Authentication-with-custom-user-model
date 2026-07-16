from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
User=get_user_model()
from .models import EmailOTP
from django.utils import timezone

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,validators=[validate_password])
    password2 = serializers.CharField(write_only=True,)
    class Meta:
        model=User
        fields=('email','first_name','last_name','phone','password','password2',)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2'] :
            raise serializers.ValidationError({"Password doesn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        password=validated_data.pop('password')
        user=User(**validated_data)
        user.set_password(password)
        user.is_verified=False
        user.save()
        return user
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data=super().validate(attrs)
        if not self.user.is_verified :
            raise serializers.ValidationError(
                {"Account is not verified. Please check your email"}
            )
        return data
    
class PasswordChangeSerializer(serializers.Serializer):
    old_password=serializers.CharField()
    new_password=serializers.CharField(validators=[validate_password])

    def validate_old_password(self,value):
        user=self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password doesn't match")
        
        return value
    

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=("email","first_name","last_name","phone","role","is_verified")
        read_only_fields=("email","role","is_verified")


class EmailVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, attrs):
        email = attrs["email"]
        otp = attrs["otp"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"email": "Invalid email."}
            )

        if user.is_verified:
            raise serializers.ValidationError(
                {"email": "This account is already verified."}
            )

        try:
            email_otp = EmailOTP.objects.get(
                user=user,
                otp=otp
            )
        except EmailOTP.DoesNotExist:
            raise serializers.ValidationError(
                {"otp": "Invalid OTP."}
            )

        if email_otp.expires_at < timezone.now():
            email_otp.delete()

            raise serializers.ValidationError(
                {"otp": "OTP has expired."}
            )

        attrs["user"] = user
        attrs["email_otp"] = email_otp

        return attrs