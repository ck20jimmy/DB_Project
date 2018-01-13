from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
class Personnel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, editable=False)
    email = models.EmailField()
    name = models.CharField(max_length=50)
class Accounts(models.Model):
    personnel_ID = models.ForeignKey('Personnel',on_delete=models.SET_DEFAULT,default="Out-of-management")
    username = models.CharField(max_length=50, primary_key=True)
    privilege = models.CharField(max_length=50)
    machine = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=50)
class Access_to_server(models.Model):
    username = models.ForeignKey('Personnel', on_delete=models.CASCADE, primary_key=True)
    server_ID = models.ForeignKey('Servers', on_delete=models.CASCADE, primary_key=True)
class Access_to_service(models.Model):
    username = models.ForeignKey('Personnel', on_delete=models.CASCADE, primary_key=True)
    service_ID = models.ForeignKey('Services', on_delete=models.CASCADE, primary_key=True)
class Access_to_switches(models.Model):
    username = models.ForeignKey('Personnel', on_delete=models.CASCADE, primary_key=True)
    switches_ID = models.ForeignKey('Switches', on_delete=models.CASCADE, primary_key=True)



class Servers(models.Model):
    ip = models.CharField(max_length=15)
class Services(models.Model):
    server_ID = models.ForeignKey('Servers', on_delete=models.CASCADE)
class Switches(models.Model):
    ip = models.CharField(max_length=15)

                                

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
        instance.account.save()

