from django.db import models

from auth_api.models import Student


class Course(models.Model):
    image_preview = models.ImageField(
        upload_to="images/",
        help_text="Images are here -> images/",
        null=True,
        blank=True,
        verbose_name="изображение",
    )
    description = models.CharField(max_length=1024, verbose_name="описание")

    name = models.CharField(max_length=256, verbose_name="название курса")
    lessons = models.ManyToManyField("Lesson", verbose_name="уроки")
    owner = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    image_preview = models.ImageField(
        upload_to="images/",
        help_text="Images are here -> images/",
        null=True,
        blank=True,
        verbose_name="изображение",
    )
    description = models.CharField(max_length=1024, verbose_name="описание")
    name = models.CharField(max_length=256, verbose_name="название урока")
    course_name = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="курс"
    )
    video_link = models.CharField(max_length=256, verbose_name="ссылка на видео")

    owner = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Payment(models.Model):
    PAYMENT_METHOD = [
        ("cash", "наличные"),
        ("bank_transfer", "перевод"),
    ]

    user = models.ForeignKey(
        Student, on_delete=models.DO_NOTHING, verbose_name="студент"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
        verbose_name="курс",
    )
    pay_date = models.DateTimeField(auto_now_add=True, verbose_name="дата оплаты")
    payment_amount = models.DecimalField(
        decimal_places=2, max_digits=10, verbose_name="сумма оплаты"
    )
    payment_method = models.CharField(
        max_length=13, choices=PAYMENT_METHOD, verbose_name="метод оплаты"
    )

    def __str__(self):
        return f"{self.user}: {self.pay_date} - {self.payment_amount} - {self.payment_method}"


class Subscription(models.Model):
    """Модель для описания подписки на обновления курса для пользователя"""

    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               related_name='updates',
                               verbose_name='Курс')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='updates',
                             verbose_name='Пользователь')

    def __str__(self):
        return f"{self.user.email} подписан на обновления курса {self.course.name}"

    class Meta:
        unique_together = ('course', 'user')
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


