from django.db import models
from django.conf import settings
# Create your models here.

class ContactUs(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name=models.CharField(max_length=222)
    email=models.EmailField()
    subject=models.CharField(max_length=222)
    message=models.TextField()

    def __str__(self):
        return self.user