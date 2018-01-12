from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from web.models import Account

# Register your models here.
class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    
    class Meta:
        model = Account
        fields = ('email', 'name')
    
    def check_password(self):
    
        pwd = self.cleaned_data.get('password1')
        confirm = self.cleaned_data.get('password2')
        if pwd & confirm & pwd != confirm:
            raise forms.ValidationError("Passwords don't match!")
        return confirm

    def save(self, commit=True):
        
        user = super().save(commit = False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdmin(BaseUserAdmin):

    add_form = UserCreationForm
    list_display = ('email', 'name', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
        'classes': ('wide',),
        'fields': ('email', 'name', 'pwd', 'confirm')})
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(Account, UserAdmin)

admin.site.unregister(Group)

