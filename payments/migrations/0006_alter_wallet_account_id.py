# Generated by Django 4.1.7 on 2023-03-21 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0005_alter_wallet_account_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="wallet",
            name="account_id",
            field=models.IntegerField(default=1, null=True),
        ),
    ]
