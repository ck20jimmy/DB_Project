from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
class Personnel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, editable=False)
    email = models.EmailField()
    name = models.CharField(max_length=50)
    def __str__(self):
        return '%s (%s)' % (self.name, self.email)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Personnel.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.personnel.email = instance.email
    instance.personnel.save()

class Account(models.Model):
    personnel_ID = models.ForeignKey('Personnel',on_delete=models.SET_NULL,null=True)
    username = models.CharField(max_length=50)
    privilege = models.CharField(max_length=50)
    machine = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    def __str__(self):
        return self.username + '@' + self.machine

class Server(models.Model):
    ip = models.CharField(max_length=15)
class Service(models.Model):
    server_ID = models.ForeignKey('Server', on_delete=models.CASCADE)
class Switch(models.Model):
    ip = models.CharField(max_length=15)

class Access_to_server(models.Model):
    class Meta:
        unique_together = (('username', 'server_ID'),)
    username = models.ForeignKey('Personnel', on_delete=models.CASCADE)
    server_ID = models.ForeignKey('Server', on_delete=models.CASCADE)
class Access_to_service(models.Model):
    class Meta:
        unique_together = (('username', 'service_ID'),)
    username = models.ForeignKey('Personnel', on_delete=models.CASCADE)
    service_ID = models.ForeignKey('Service', on_delete=models.CASCADE)
class Access_to_switches(models.Model):
    class Meta:
        unique_together = (('username', 'switches_ID'),)
    username = models.ForeignKey('Personnel', on_delete=models.CASCADE)
    switches_ID = models.ForeignKey('Switch', on_delete=models.CASCADE)

                               


