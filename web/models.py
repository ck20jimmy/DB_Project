from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
class Personnel(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
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
    id = models.IntegerField(primary_key=True)
    personnel_id = models.ForeignKey('Personnel',on_delete=models.SET_NULL,null=True)
    username = models.CharField(max_length=50)
    privilege = models.CharField(max_length=50)
    machine = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    def __str__(self):
        return self.username + '@' + self.machine

class Server(models.Model):
    id = models.IntegerField(primary_key=True)
    slot_num = models.IntegerField()
    cabinet_num = models.IntegerField()
    spec = models.CharField(max_length=300)
    brand_and_model = models.CharField(max_length=100)

class Service(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    server_id = models.ForeignKey('Server', on_delete=models.CASCADE)
    port_id = models.IntegerField()
    
class Switch(models.Model):
    id = models.IntegerField(primary_key=True)
    ip = models.IntegerField()
    slot_num = models.IntegerField()  
    brand_and_model = models.CharField(max_length=100)
    cabinet_num = models.IntegerField()

class Interface(models.Model):
    id = models.IntegerField(primary_key=True)
    ip = models.IntegerField()
    hostname = models.CharField(max_length=100)
    server_id = models.ForeignKey('Server', on_delete=models.CASCADE)
    port_id = models.ForeignKey('Port', on_delete=models.CASCADE)
    service_id = models.ForeignKey('Service', on_delete=models.CASCADE)

class Vlan(models.Model):
    id = models.IntegerField(primary_key=True)

class Port(models.Model):
    id = models.IntegerField(primary_key=True)
    switch_id = models.ForeignKey('Switch', on_delete=models.CASCADE)

class Access_to_server(models.Model):
    class Meta:
        unique_together = (('username', 'server_id'),)
    username = models.ForeignKey('Account', on_delete=models.CASCADE)
    server_id = models.ForeignKey('Server', on_delete=models.CASCADE)

class Access_to_service(models.Model):
    class Meta:
        unique_together = (('username', 'service_id'),)
    username = models.ForeignKey('Account', on_delete=models.CASCADE)
    service_id = models.ForeignKey('Service', on_delete=models.CASCADE)

class Access_to_switch(models.Model):
    class Meta:
        unique_together = (('username', 'switch_id'),)
    username = models.ForeignKey('Account', on_delete=models.CASCADE)
    switch_id = models.ForeignKey('Switch', on_delete=models.CASCADE)

class Vlan_to_port(models.Model):
    class Meta:
        unique_together = (('vlan_id', 'port_id'),)
    vlan_id = models.ForeignKey('Vlan', on_delete=models.CASCADE)
    port_id = models.ForeignKey('Port', on_delete=models.CASCADE)

class Vlan_to_interface(models.Model):
    class Meta:
        unique_together = (('vlan_id', 'interface_id'),)
    vlan_id = models.ForeignKey('Vlan', on_delete=models.CASCADE)
    interface_id = models.ForeignKey('Interface', on_delete=models.CASCADE)
