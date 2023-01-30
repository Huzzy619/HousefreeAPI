# Generated by Django 4.1.5 on 2023-01-30 01:42

from django.db import migrations, models
import django.db.models.deletion
import utils.paths.path_helpers


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Blog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=500)),
                ("content", models.TextField()),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("Spotlight", "Spotlight"),
                            ("Buying & Selling", "Buying & Selling"),
                            ("Renting", "Renting"),
                            ("Tips & Advice", "Tips & Advice"),
                        ],
                        max_length=200,
                    ),
                ),
                ("featured", models.BooleanField(default=False)),
                ("date_published", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["-date_published"],
            },
        ),
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "img",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=utils.paths.path_helpers.get_blogs_image_path,
                    ),
                ),
                (
                    "blog",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="blog.blog",
                    ),
                ),
            ],
        ),
    ]
