# Generated by Django 3.2.9 on 2022-08-05 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_rename_notifications_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='status_read',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='profiledata',
            name='telephone_verified',
            field=models.BooleanField(default=False),
        ),
    ]
