# Generated by Django 3.0.8 on 2020-08-14 05:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bids', '0006_auto_20200813_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='bidlisting',
            name='active',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
