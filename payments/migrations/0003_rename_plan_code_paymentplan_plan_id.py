# Generated by Django 4.1.7 on 2023-03-21 03:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0002_bankdetail_paymentplan"),
    ]

    operations = [
        migrations.RenameField(
            model_name="paymentplan",
            old_name="plan_code",
            new_name="plan_id",
        ),
    ]
