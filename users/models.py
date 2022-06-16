
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, GroupManager
from django.utils.translation import gettext_lazy as _



GENDERS = (
    ('male', _('Male')),
    ('female', _('Female')),
)


class UserRoles(models.IntegerChoices):
    MANAGER = 1, 'MANAGER'
    WORKER = 2, 'WORKER'


class UserInfo(AbstractUser):
    section = models.CharField(max_length=255, null=True, blank=True)
    position = models.CharField(max_length=255, null=True, blank=True)
    full_name = models.CharField(max_length=400,null=True)
    date_of_birthday = models.CharField(max_length=50,default='',null=True)
    gender = models.CharField(choices=GENDERS, max_length=6, null=True, blank=True, )
    degree = models.CharField(max_length=255, null=True, blank=True)
    inps_number = models.CharField(null=True,default=0,max_length=60)
    phone_number = models.CharField(max_length=250,default='')
    user_role = models.IntegerField(choices=UserRoles.choices,default=2,null=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return f'{self.full_name}'

 