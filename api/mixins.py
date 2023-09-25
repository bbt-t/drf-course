from django.db import models


class Info(models.Model):
    image_preview = models.ImageField(
        upload_to="images/",
        help_text="Images are here -> images/",
        null=True,
        blank=True,
        verbose_name="изображение",
    )
    description = models.CharField(max_length=1024, verbose_name="описание")
