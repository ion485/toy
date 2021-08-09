from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.base_user import BaseUserManager

from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)

from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('이메일은 필수 항목입니다.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('권한 설정 실패 is_staff')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('권한 설정 실패 superuser')

        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email', unique=True)
    name = models.CharField('이름', max_length=30, blank=True)
    is_staff = models.BooleanField('권한', default=False)
    date = models.DateTimeField('가입일', default=timezone.now)
    location = models.CharField('소셜', max_length=30, default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    # REQUIRED_FIELDS = ['name', 'location', 'is_staff']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        swappable = 'AUTH_USER_USER'

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

