from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

class Profile(models.Model):
    token = models.CharField(max_length=255,null=False)

    class Meta:
        db_table = 'profile'

class User(AbstractUser):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True)
    modified = models.DateTimeField(auto_now=True)
    email = models.EmailField(null=False, unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (email, )
    class Meta:
        db_table = 'user'



class Address(models.Model):
    street = models.CharField(max_length=50, null=False)
    number = models.CharField(max_length=20, null=False)
    district = models.CharField(max_length=50, null=False)
    city = models.CharField(max_length=50, null=False)
    state = models.CharField(max_length=2, null=False)
    country = models.CharField(max_length=50, null=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = 'address'



