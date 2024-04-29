# Generated by Django 5.0.4 on 2024-04-23 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='tweet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tweet_id', models.CharField(max_length=100, unique=True)),
                ('text', models.TextField(max_length=100)),
                ('created_at', models.DateTimeField()),
                ('tweet_link', models.URLField()),
                ('user_screen_name', models.CharField(max_length=100)),
            ],
        ),
    ]
