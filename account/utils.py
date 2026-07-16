import random
from datetime import timedelta
from django.utils import timezone
from .models import EmailOTP
from django.core.mail import send_mail
from django.conf import settings

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