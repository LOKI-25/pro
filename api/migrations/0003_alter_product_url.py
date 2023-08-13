# Generated by Django 4.1.7 on 2023-08-13 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_user_managers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='url',
            field=models.URLField(error_messages={'unique': 'This URL is already scraped.'}, unique=True),
        ),
    ]