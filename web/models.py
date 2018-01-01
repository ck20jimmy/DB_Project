from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
# Create your models here.
class AccountManager(BaseUserManager):
    
    def create_user(self, email, name, password=None):
    
        if not email:
            raise ValueError('Missing Required Field: Email')
        user = self.model(
            email = self.normalized_email(email),
            name = name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, name, password):
        
        user = self.create_user(email, name = name, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user



class Account(AbstractBaseUser):
    
    email = models.EmailField(primary_key=True)
    name = models.CharField(max_length=40)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = AccountManager()
    
    #With default privileges, must be modified before use.
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    @property
    def is_staff(self):
        return self.is_admin
