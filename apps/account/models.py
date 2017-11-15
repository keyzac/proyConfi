from faulthandler import _read_null
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import PermissionsMixin, BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser,
                     **extra_fields):
        user = self.model(email=email, is_active=True,
                          is_staff=is_staff, is_superuser=is_superuser,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='user', blank=True, null=True)
    objects = UserManager()
    is_enabled = models.BooleanField(default=True, verbose_name='Habilitar Usuario')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"


class Songbook(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = "Cancionero"
        verbose_name_plural = "Cancioneros"

    def __str__(self):
        return self.name

# Create your models here.
