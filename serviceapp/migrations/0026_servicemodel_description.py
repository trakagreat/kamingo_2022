# Generated by Django 4.0.1 on 2022-01-29 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serviceapp', '0025_servicemodel_address_alter_address_address_line1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicemodel',
            name='description',
            field=models.CharField(blank=True, max_length=600, null=True),
        ),
    ]
