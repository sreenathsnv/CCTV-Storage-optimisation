# Generated by Django 5.0.3 on 2024-03-07 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_footages_footage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='footages',
            name='footage',
            field=models.FileField(upload_to='uploads/%d-%m-%y'),
        ),
    ]
