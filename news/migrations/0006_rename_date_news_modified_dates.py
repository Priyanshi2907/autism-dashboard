# Generated by Django 5.0.4 on 2024-05-12 06:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_remove_news_description_remove_news_modified_dates_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='news',
            old_name='date',
            new_name='modified_dates',
        ),
    ]