# Generated by Django 3.0.8 on 2020-08-11 06:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bids', '0004_auto_20200810_0608'),
    ]

    operations = [
        migrations.AddField(
            model_name='bidlisting',
            name='imageUrl',
            field=models.URLField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
