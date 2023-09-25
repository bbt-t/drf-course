from django.core.management import BaseCommand

from api.models import Student


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = Student.objects.create(
            email="admin@admin.com",
            first_name="Ad",
            last_name="Min",
            is_staff=True,
            is_superuser=True,
        )

        user.set_password("123")
        user.save()
