from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from api.mixins import Info


class Student(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name="почта")
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

    class Meta:
        indexes = [
            models.Index(fields=["email"]),
        ]


class Course(Info):
    name = models.CharField(max_length=256, verbose_name="название курса")


class Lesson(Info):
    name = models.CharField(max_length=256, verbose_name="название урока")
    video_link = models.CharField(max_length=256, verbose_name="ссылка на видео")

