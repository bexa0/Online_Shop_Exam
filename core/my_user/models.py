from django.db import models
from django.contrib.auth.models import User


class AbstractUserClass(User):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='Users')
    avatar = models.ImageField(upload_to='users', null=True, blank=True)
