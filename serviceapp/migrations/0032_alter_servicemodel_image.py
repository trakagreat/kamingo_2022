# Generated by Django 4.0.1 on 2022-06-14 09:13

from django.db import migrations, models
import serviceapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('serviceapp', '0031_alter_servicemodel_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicemodel',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to=serviceapp.models.path_and_rename),
        ),
    ]
