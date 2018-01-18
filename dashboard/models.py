from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
class Personnel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False, null=True)
    email = models.EmailField()
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Personnel.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.personnel.email = instance.email
    instance.personnel.save()

class Server_account(models.Model):
    personnel = models.ForeignKey('Personnel', on_delete=models.SET_NULL, null=True)  
    username = models.CharField(max_length=50, null=True)
    privilege = models.CharField(max_length=50, null=True)
    server_name = models.ForeignKey('Server', on_delete=models.CASCADE)
    password = models.CharField(max_length=50, null=True)
    def __str__(self):
        return '{}@{}'.format(self.username, self.server_name)

class Switch_account(models.Model):
    personnel = models.ForeignKey('Personnel',on_delete=models.SET_NULL, null=True)  
    username = models.CharField(max_length=50, null=True)
    privilege = models.CharField(max_length=50, null=True)
    switch_name = models.ForeignKey('Switch', on_delete=models.CASCADE)
    password = models.CharField(max_length=50, null=True)
    def __str__(self):
        return '{}@{}'.format(self.username, self.switch_name)

class Server(models.Model):
    name = models.CharField(max_length=100)
    slot_num = models.IntegerField(null=True)
    cabinet_num = models.IntegerField(null=True)
    spec = models.CharField(max_length=300, null=True)
    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=50, null=True)
    server_name = models.ForeignKey('Server', on_delete=models.CASCADE, null=True, blank=True)
    port = models.IntegerField(null=True)
    interface_name = models.ForeignKey('Interface', on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return '{}@{}'.format(self.name, self.server_name)

class Switch(models.Model):
    name = models.CharField(max_length=100, null=True)
    ip = models.CharField(max_length=20, null=True)
    slot_num = models.IntegerField(null=True)  
    cabinet_num = models.IntegerField(null=True)
    def __str__(self):
        return self.name

class Interface(models.Model):
    name = models.CharField(max_length=20, null=True)
    ip = models.CharField(max_length=20, null=True)
    hostname = models.CharField(max_length=100, null=True)
    server_name = models.ForeignKey('Server', on_delete=models.CASCADE)
    switch_port = models.ForeignKey('Port', on_delete=models.CASCADE)
    def __str__(self):
        return '{}@{}'.format(self.name, self.server_name)


class Port(models.Model):
    switch_port_id = models.IntegerField(null=True)
    switch_name = models.ForeignKey('Switch', on_delete=models.CASCADE)
    def __str__(self):
        return '{} port{}'.format(self.switch_name, self.switch_port_id)

class Access_to_service(models.Model):
    class Meta:
        unique_together = (('username', 'service_name'),)
    username = models.ForeignKey('Server_account', on_delete=models.CASCADE)
    service_name = models.ForeignKey('Service', on_delete=models.CASCADE)

class Vlan_to_interface(models.Model):
    class Meta:
        unique_together = (('vlan_id', 'interface_name'),)
    vlan_id = models.IntegerField(null=True)
    interface_name = models.ForeignKey('Interface', on_delete=models.CASCADE)
