from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from .managers import CustomUserManager
from django.conf import settings

class User(AbstractUser):
    ROLE=[
        ('admin','Admin'),
        ('manager','Manager'),
        ('staff','Staff'),
        ('customer','Customer'),
    ]

    username=None
    email=models.EmailField("Email_Address",unique=True)
    phone=models.CharField(max_length=15,blank=True,null=True)
    role=models.CharField(
        max_length=20,
        choices=ROLE,
        default='customer',
    )
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD="email"
    REQUIRED_FIELDS=[]  

    objects=CustomUserManager()
    
    def __str__(self):
        return self.email


class EmailOTP(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="email_otps")
    otp=models.CharField(max_length=6)
    created_at=models.DateTimeField(auto_now_add=True)
    expires_at=models.DateTimeField()

    def __str__(self):
        return f"{self.user.email}-{self.otp}"

    