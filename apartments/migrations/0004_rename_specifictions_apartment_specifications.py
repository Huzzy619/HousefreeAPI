# Generated by Django 4.1.4 on 2023-01-02 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("apartments", "0003_remove_apartment_features_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="apartment",
            old_name="specifictions",
            new_name="specifications",
        ),
    ]
