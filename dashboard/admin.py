from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from dashboard.models import *

admin.site.register((Server_account, Switch_account, Personnel, Server, Service, Switch, Interface, Port, Access_to_service, Vlan_to_interface),)
admin.site.unregister(Group)
