# Generated by Django 5.0.4 on 2024-04-25 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0006_alter_tweet_user_followers_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='user_followers_count',
            field=models.IntegerField(default=0),
        ),
    ]
