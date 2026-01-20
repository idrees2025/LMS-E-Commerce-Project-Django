from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='pfp/')
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user

class CustomUser(AbstractUser):
    stripe_customer_id=models.CharField(max_length=222)