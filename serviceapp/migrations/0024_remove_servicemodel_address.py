# Generated by Django 4.0.1 on 2022-01-28 15:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('serviceapp', '0023_remove_servicemodel_address2_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicemodel',
            name='address',
        ),
    ]
