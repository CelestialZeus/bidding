# Generated by Django 3.0.8 on 2020-08-16 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bids', '0010_auto_20200815_0516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidlisting',
            name='imageUrl',
            field=models.URLField(blank=True),
        ),
    ]
