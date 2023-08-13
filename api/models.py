from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects=CustomUserManager()

    def __str__(self):
        return self.email

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField(max_length=5000,unique=True,error_messages={
            'unique': "This URL is already scraped.",
        })
    title = models.CharField(max_length=1000)
    price = models.CharField(max_length=1000)
    description = models.TextField(blank=True, null=True)
    reviews_count = models.IntegerField()
    ratings_count = models.IntegerField()
    ratings = models.FloatField()
    media_count = models.IntegerField()

    def __str__(self):
        return self.title