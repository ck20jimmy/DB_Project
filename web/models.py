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


class Server_account(models.Model):
    personnel_ID = models.ForeignKey('Personnel',on_delete=models.SET_NULL,null=True)  
    username = models.CharField(max_length=50)
    privilege = models.CharField(max_length=50)
    server_ID = models.ForeignKey('Server',  on_delete=models.CASCADE)
    password = models.CharField(max_length=50)
    def __str__(self):
        return self.username + '@' + self.server_ID

class Switch_account(models.Model):
    personnel_ID = models.ForeignKey('Personnel',on_delete=models.SET_NULL,null=True)  
    username = models.CharField(max_length=50)
    privilege = models.CharField(max_length=50)
    switch_ID = models.ForeignKey('Switch', on_delete=models.CASCADE)
    password = models.CharField(max_length=50)
    def __str__(self):
        return self.username + '@' + self.switch_ID

class Access_to_server(models.Model):
    class Meta:
        unique_together = (('username', 'server_id'),)
    username = models.ForeignKey('Personnel', on_delete=models.CASCADE)
    server_id = models.ForeignKey('Server', on_delete=models.CASCADE)


class Access_to_service(models.Model):
    class Meta:
        unique_together = (('username', 'service_id'),)
    username = models.ForeignKey('Personnel', on_delete=models.CASCADE)
    service_id = models.ForeignKey('Service', on_delete=models.CASCADE)


class Access_to_switches(models.Model):
    class Meta:
        unique_together = (('username', 'switches_id'),)
    username = models.ForeignKey('Personnel', on_delete=models.CASCADE)
    switches_id = models.ForeignKey('Switch', on_delete=models.CASCADE)


#New table
class Server(models.Model):
    slot_num = models.IntegerField(null=True)
    spec = models.TextField(null=True)
    brand_and_model = models.CharField(max_length=50,null=True)
    cabinet_num = models.IntegerField(null=True)


class Service(models.Model):
    name = models.CharField(max_length=50,null=True)
    server_id = models.ForeignKey(Server,on_delete=models.CASCADE)
    port_id = models.IntegerField(null=True)
    interface_id = models.ForeignKey('Interface',on_delete=models.CASCADE,null=True)

    
class Interface(models.Model):
    ip = models.CharField(max_length=16,null=True)
    hostname = models.CharField(max_length=50,null=True)
    server_id = models.ForeignKey(Server,on_delete=models.CASCADE)
    port_id = models.ForeignKey('Port',on_delete=models.CASCADE)
    service_id = models.ForeignKey(Service,on_delete=models.CASCADE)


class Port(models.Model):
    switch_id = models.ForeignKey('Switch',on_delete=models.CASCADE)
    switch_port_id = models.IntegerField(null=True)

class Switch(models.Model):
    ip = models.CharField(max_length=16,null=True)
    slot_num = models.IntegerField(null=True)
    brand_and_model = models.CharField(max_length=50,null=True)
    cabinet_num = models.IntegerField(null=True)

