# Generated by Django 4.2.7 on 2024-04-23 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0003_alter_tweet_tweet_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='tweet_id',
            field=models.CharField(max_length=100),
        ),
    ]
