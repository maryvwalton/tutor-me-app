# Generated by Django 4.1.7 on 2023-03-22 22:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_merge_20230320_2152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='professor',
        ),
    ]