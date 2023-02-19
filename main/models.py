from random import sample

from django.apps import apps
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.password_validation import validate_password


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    password = models.CharField(_("password"), max_length=128, validators=[validate_password])
    email = models.EmailField(_("email address"), unique=True)
    phone_number = PhoneNumberField(blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class Order(models.Model):
    number = models.IntegerField(verbose_name=_('Order ID'))
    title = models.CharField(max_length=200)
    text = models.TextField()
    file = models.FileField(upload_to='files/', blank=True)
    client = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL, null=True,
        limit_choices_to={'is_staff': False}
    )
    date_created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        number = int(''.join(map(str, sample(range(1, 10), 8))))
        while Order.objects.filter(number=number).exists():
            number = int(''.join(map(str, sample(range(1, 10), 8))))
        setattr(self, 'number', number)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.number)

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")


class Answer(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    title = models.CharField(max_length=400, blank=True)
    text = models.TextField(blank=True)
    file_format = models.CharField(max_length=100)
    file = models.FileField(upload_to='files/')
    comment = models.CharField(max_length=500)
    date_created = models.DateTimeField(auto_now_add=True)

    creator = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL, null=True,
        limit_choices_to={'is_staff': True}
    )

    def __str__(self):
        return f"{self.order}"

    class Meta:
        verbose_name = _("svarar")
        verbose_name_plural = _("svarars")


class Message(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    text = models.CharField(max_length=400)
    creator = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = _("message")
        verbose_name_plural = _("messages")
