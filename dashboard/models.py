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
    personnel_id = models.ForeignKey('Personnel', on_delete=models.SET_NULL, null=True)  
    username = models.CharField(max_length=50, null=True)
    privilege = models.CharField(max_length=50, null=True)
    server_id = models.ForeignKey('Server', on_delete=models.CASCADE)
    password = models.CharField(max_length=50, null=True)
    #def __str__(self):
        #return self.username + '@' + self.server_id

class Switch_account(models.Model):
    personnel_id = models.ForeignKey('Personnel',on_delete=models.SET_NULL, null=True)  
    username = models.CharField(max_length=50, null=True)
    privilege = models.CharField(max_length=50, null=True)
    switch_id = models.ForeignKey('Switch', on_delete=models.CASCADE)
    password = models.CharField(max_length=50, null=True)
    #def __str__(self):
        #return str(self.username) + '@' + str(self.switch_id)

class Server(models.Model):
    slot_num = models.IntegerField(null=True)
    cabinet_num = models.IntegerField(null=True)
    spec = models.CharField(max_length=300, null=True)
    brand_and_model = models.CharField(max_length=100, null=True)

class Service(models.Model):
    name = models.CharField(max_length=50, null=True)
    server_id = models.ForeignKey('Server', on_delete=models.CASCADE)
    port_id = models.IntegerField(null=True)
    interface_id = models.ForeignKey('Interface', on_delete=models.CASCADE)

class Switch(models.Model):
    ip = models.CharField(max_length=20, null=True)
    slot_num = models.IntegerField(null=True)  
    brand_and_model = models.CharField(max_length=100, null=True)
    cabinet_num = models.IntegerField(null=True)

class Interface(models.Model):
    ip = models.CharField(max_length=20, null=True)
    hostname = models.CharField(max_length=100, null=True)
    server_id = models.ForeignKey('Server', on_delete=models.CASCADE)
    port_id = models.ForeignKey('Port', on_delete=models.CASCADE)

class Port(models.Model):
    switch_port_id = models.IntegerField(null=True)
    switch_id = models.ForeignKey('Switch', on_delete=models.CASCADE)

class Access_to_service(models.Model):
    class Meta:
        unique_together = (('username', 'service_id'),)
    username = models.ForeignKey('Server_account', on_delete=models.CASCADE)
    service_id = models.ForeignKey('Service', on_delete=models.CASCADE)

class Vlan_to_interface(models.Model):
    class Meta:
        unique_together = (('vlan_id', 'interface_id'),)
    vlan_id = models.IntegerField(null=True)
    interface_id = models.ForeignKey('Interface', on_delete=models.CASCADE)
