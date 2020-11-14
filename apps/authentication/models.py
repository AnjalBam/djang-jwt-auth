from django.db import models
from django.contrib.auth.models import AbstractUser


class MyCustomUser(AbstractUser):
  date_joined = models.DateTimeField(auto_now_add=True)
  date_modified = models.DateTimeField(auto_now=True)
  email = models.EmailField(unique=True, db_index=True)
  username = models.CharField(max_length=255, unique=True, db_index=True)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username']

  user_permissions = None
  groups = None
  

class Profile(models.Model):
  user = models.OneToOneField(MyCustomUser, on_delete=models.CASCADE)
  profile_pic = models.ImageField(upload_to='profile_images/')