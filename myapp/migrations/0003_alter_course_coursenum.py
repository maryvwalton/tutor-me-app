# Generated by Django 4.1.7 on 2023-03-20 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0002_alter_sessionrequest_student"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course", name="coursenum", field=models.IntegerField(),
        ),
    ]
