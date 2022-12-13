from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models

from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    proxy = True
    username = models.CharField(_('username'), max_length=15, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    phone_regex = RegexValidator(regex=r'^\+(?:[0-9] ?){6,14}[0-9]$', message="+905304440044")
    phone_number = models.CharField(validators=[phone_regex], max_length=17)  # validators should be a list
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=False)
    is_superuser = models.BooleanField(_('superuser'), default=False)
    is_staff = models.BooleanField(_('staff'), default=False)
    # avatar = models.ImageField(upload_to='media/avatars/', null=True, blank=True, default='avatars/ppic.png')

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'phone_number']

    class Meta:
        db_table = 'auth_user'

    @classmethod
    def create(cls, first_name, last_name, email, phone_number, password):
        return cls(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, password=password)

    @property
    def full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def serialize(self):
        return {
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "date_joined": self.date_joined
        }