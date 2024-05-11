# Generated by Django 5.0.4 on 2024-05-11 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0008_tweet_country_tweet_entity_tweet_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweet',
            name='entity',
        ),
        migrations.RemoveField(
            model_name='tweet',
            name='favorite_count',
        ),
        migrations.RemoveField(
            model_name='tweet',
            name='hashtags',
        ),
        migrations.RemoveField(
            model_name='tweet',
            name='lang',
        ),
        migrations.RemoveField(
            model_name='tweet',
            name='reach',
        ),
        migrations.RemoveField(
            model_name='tweet',
            name='retweet_count',
        ),
        migrations.RemoveField(
            model_name='tweet',
            name='sentiment',
        ),
        migrations.RemoveField(
            model_name='tweet',
            name='user_friends_count',
        ),
        migrations.RemoveField(
            model_name='tweet',
            name='user_location',
        ),
        migrations.AddField(
            model_name='tweet',
            name='profile_pic',
            field=models.URLField(blank=True, null=True),
        ),
    ]