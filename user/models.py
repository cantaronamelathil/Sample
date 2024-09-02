from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserModel(AbstractUser):
    ADMIN = 'admin'
    STAFF = 'staff'
    ROLE_CHOICES=[
        (ADMIN,'admin'),
        (STAFF,'staff'),
    ]
    role = models.CharField(max_length=10,choices=ROLE_CHOICES,default=STAFF)
    profile_image = models.ImageField(upload_to = 'profile_images/',blank =True,null=True)
    
    def is_admin(self):
        return self.role == self.ADMIN
    def is_staff(self):
        return self.role ==  self.STAFF
    