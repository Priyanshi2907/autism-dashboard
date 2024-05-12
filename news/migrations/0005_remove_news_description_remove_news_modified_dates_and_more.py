# Generated by Django 5.0.4 on 2024-05-12 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_alter_news_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='description',
        ),
        migrations.RemoveField(
            model_name='news',
            name='modified_dates',
        ),
        migrations.RemoveField(
            model_name='news',
            name='sentiment',
        ),
        migrations.AddField(
            model_name='news',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
    ]