from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserManager


class Department(models.Model):

    name = models.CharField(
        'Наименование',
        max_length=255,
    )
    description = models.TextField(
        'Описание',
        max_length=500,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):

    HR = 'hr'
    CHIEF = 'chief'
    EMPLOYEE = 'employee'

    ROLES = (
        (HR, 'HR'),
        (CHIEF, 'Руководитель'),
        (EMPLOYEE, 'Работник')
    )

    email = models.EmailField(
        unique=True,
        max_length=255,
        blank=False
    )
    first_name = models.CharField(
        _('first name'),
        max_length=30,
        blank=True
    )
    last_name = models.CharField(
        _('last name'),
        max_length=150,
        blank=True
    )
    department = models.ForeignKey(
        Department,
        verbose_name='Отдел',
        related_name='employees',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    role = models.CharField(
        'Роль',
        choices=ROLES,
        max_length=10,
        default='employee',
        db_index=True
    )
    avatar = models.ImageField(
        upload_to='users/avatars/',
        blank=True,
        null=True
    )
    about = models.TextField(
        'О себе',
        max_length=500,
        blank=True,
        null=True
    )
    phone = PhoneNumberField(
        'Телефон',
        blank=True
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False
    )
    is_active = models.BooleanField(
        _('active'),
        default=True
    )
    date_joined = models.DateTimeField(
        _('date joined'),
        default=timezone.now,
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'

    @property
    def is_hr(self):
        return self.role == self.HR

    @property
    def is_chief(self):
        return self.role == self.CHIEF

    @property
    def is_employee(self):
        return self.role == self.EMPLOYEE

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
