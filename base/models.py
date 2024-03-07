from django.db import models
from django.contrib.auth.models import AbstractUser

from .manager import UserManager

class CustomUser(AbstractUser):

    email = models.EmailField(unique = True)
    username = models.CharField(max_length = 100)
    timestamp = models.DateTimeField(auto_now_add = True)
    
    is_admin = models.BooleanField(default = False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['timestamp']
    def __str__(self) -> str:
        return self.username
    @property
    def is_admin(self):
        return self.is_admin



class Footages(models.Model):

    thumbnail = models.ImageField(default= "images/thumbnail.png" )
    footage =  models.FileField(upload_to="uploads/%d-%m-%y")
    timestamp = models.DateField(auto_now = True)

    user = models.ForeignKey(CustomUser,on_delete = models.CASCADE)

