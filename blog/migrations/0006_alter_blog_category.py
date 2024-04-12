# Generated by Django 5.0.2 on 2024-03-24 10:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0005_alter_blog_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blog",
            name="category",
            field=models.CharField(
                choices=[
                    ("spotlight", "Spotlight"),
                    ("buying_and_selling", "Buying & Selling"),
                    ("renting", "Renting"),
                    ("tips_and_advice", "Tips & Advice"),
                ],
                max_length=200,
            ),
        ),
    ]