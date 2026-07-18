import random
from datetime import timedelta
from django.utils import timezone
from .models import EmailOTP
from django.core.mail import send_mail
from django.conf import settings

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

def genarate_email_otp(user):
    #ager otp thakle delete kore debo . amra filter use korbo jate kno error na ase otp na thakle
    EmailOTP.objects.filter(user=user).delete()

    #new otp genarate korbo
    otp=f"{random.randint(100000,999999)}"

    #expire time set korbo 
    expires_at=timezone.now()+timedelta(minutes=5)

    # now create otp object in EmailOTP model
    EmailOTP.objects.create(
        user=user,
        otp=otp,
        expires_at=expires_at,

    )
    return otp

def send_verification_email(user,otp):

    send_mail( 
        subject="Verify your Email",
        message=( 
            f"Hello {user.first_name or 'User'},\n\n"
            f"Your verification OTP is: {otp}\n\n" 
            f"This OTP will expire in 5 minutes.\n\n"
            f"If you did not create this account, please ignore this email." ),
        from_email=settings.DEFAULT_FROM_EMAIL, 
        recipient_list=[user.email], 
        fail_silently=False, 
        )
    

def send_password_reset_email(user):
    uid= urlsafe_base64_encode(
        force_bytes(user.id)
    )
    token=PasswordResetTokenGenerator().make_token(user)

    reset_link=(
        f"{settings.FRONTEND_URL}"
        f"/password-reset/{uid}/{token}/"
    )

    send_mail(
        subject="Reset Your Password.",
        message=(
            f"Hello {user.first_name},\n\n" 
            f"Click the link below to reset your password:\n\n" 
            f"{reset_link}\n\n" 
            "If you did not request this, you can ignore this email."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )