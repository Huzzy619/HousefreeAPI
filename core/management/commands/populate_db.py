import os
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import connection, utils


class Command(BaseCommand):
    help = "Populates the database with collections and products"

    def handle(self, *args, **options):
        self.stdout.write("Populating the database...")

        try:
            current_dir = os.path.dirname(__file__)
            file_path = os.path.join(current_dir, "seed.sql")
            sql = Path(file_path).read_text()

            with connection.cursor() as cursor:
                cursor.execute(sql)

            self.stdout.write(self.style.SUCCESS("Database Populated"))

        except utils.IntegrityError:

            self.stdout.write(
                self.style.ERROR(
                    "Remove Insert commands for django_content-type, django_migrations, auth-permissions, django_site"
                )
            )

            self.stdout.write(
                self.style.ERROR(
                    "If the problem persists, it means the data has already been inserted successfully."
                )
            )
