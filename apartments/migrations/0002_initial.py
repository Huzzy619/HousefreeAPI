# Generated by Django 4.1.5 on 2023-01-13 02:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("apartments", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="picture",
            name="apartment",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="pictures",
                to="apartments.apartment",
            ),
        ),
        migrations.AddField(
            model_name="media",
            name="apartment",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="videos",
                to="apartments.apartment",
            ),
        ),
        migrations.AddField(
            model_name="bookmark",
            name="apartment",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="apartments.apartment"
            ),
        ),
        migrations.AddField(
            model_name="bookmark",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="apartment",
            name="agent",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
