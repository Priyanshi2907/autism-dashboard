# Generated by Django 4.2.7 on 2024-04-23 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0002_alter_tweet_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='tweet_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]