from django.db import models
from django.contrib.auth.models import AbstractUser


class MyCustomUser(AbstractUser):
  email = models.EmailField(unique=True, db_index=True)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username']

  user_permissions = None
  groups = None
  