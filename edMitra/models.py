from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from .manager import CustomManager
# Create your models here.

class CustomManager(BaseUserManager):
    """Manager for custom user model with email as unique identifier instead of username."""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with admin privileges."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class myUser(AbstractUser):
    GENDWE_CHOICES=[
        ('M','MALE'),
        ('F','FEMALE'),
        ('O','OTHER'),
    ]
    username = None
    email = models.EmailField('Email', unique=True)
    dob = models.DateField(null=True, blank= True)
    gender = models.CharField(max_length=1,choices=GENDWE_CHOICES,blank=True,null=True)
    phone_no = models.CharField(max_length=15, null=True, blank=True)
    pin_code = models.CharField(max_length=10, null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomManager()

    def __str__(self):
        return self.email