# Generated by Django 4.1.6 on 2023-03-17 20:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_remove_student_user_remove_tutor_user_delete_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tutor',
            name='course',
        ),
        migrations.AddField(
            model_name='tutor',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.course'),
        ),
    ]