# Generated by Django 4.1.7 on 2023-03-19 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_remove_student_user_remove_tutor_user_delete_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='coursenum',
            field=models.IntegerField(),
        ),
    ]
