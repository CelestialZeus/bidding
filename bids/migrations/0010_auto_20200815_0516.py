# Generated by Django 3.0.8 on 2020-08-15 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bids', '0009_bidlisting_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='watchlist',
            field=models.ManyToManyField(blank=True, related_name='userWatchlist', to='bids.BidListing'),
        ),
        migrations.DeleteModel(
            name='Watchlist',
        ),
    ]
