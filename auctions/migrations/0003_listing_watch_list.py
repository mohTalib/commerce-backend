# Generated by Django 4.1 on 2022-09-18 18:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_rename_description_listing_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='watch_list',
            field=models.ManyToManyField(blank=True, null=True, related_name='listingForwatch', to=settings.AUTH_USER_MODEL),
        ),
    ]
