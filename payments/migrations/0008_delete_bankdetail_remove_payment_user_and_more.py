# Generated by Django 5.0.3 on 2024-04-06 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0007_bankdetail_created_at_bankdetail_updated_at_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="BankDetail",
        ),
        migrations.RemoveField(
            model_name="payment",
            name="user",
        ),
        migrations.DeleteModel(
            name="PaymentPlan",
        ),
        migrations.RemoveField(
            model_name="wallet",
            name="user",
        ),
        migrations.DeleteModel(
            name="Payment",
        ),
        migrations.DeleteModel(
            name="Wallet",
        ),
    ]
