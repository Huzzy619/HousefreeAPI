# Generated by Django 4.1.5 on 2023-01-19 00:06

from django.db import migrations, models
import utils.paths.path_helpers
import utils.validators.models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="agentdetails",
            options={"verbose_name": "Agent Detail"},
        ),
        migrations.AlterField(
            model_name="agentdetails",
            name="id_back",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=utils.paths.path_helpers.get_passport_path,
                validators=[utils.validators.models.validate_file_size],
                verbose_name="Goverment ID Back",
            ),
        ),
        migrations.AlterField(
            model_name="agentdetails",
            name="id_front",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=utils.paths.path_helpers.get_passport_path,
                validators=[utils.validators.models.validate_file_size],
                verbose_name="Goverment ID Front",
            ),
        ),
    ]
