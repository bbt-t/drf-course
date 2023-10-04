from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class Student(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name="почта", db_index=True)
    phone = PhoneNumberField(db_index=True, verbose_name="номер телефона")

    city = models.CharField(max_length=128, verbose_name="город")
    avatar_image = models.ImageField(
        upload_to="images/",
        help_text="Images are here -> images/users/",
        null=True,
        blank=True,
        verbose_name="аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "студент"
        verbose_name_plural = "студенты"

