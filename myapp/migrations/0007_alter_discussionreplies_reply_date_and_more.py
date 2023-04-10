# Generated by Django 4.1.6 on 2023-04-10 18:00

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0006_remove_tutor_slug_alter_discussionreplies_reply_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussionreplies',
            name='reply_date',
            field=models.DateTimeField(null=True, verbose_name=datetime.datetime(2023, 4, 10, 18, 0, 15, 702399, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='discussionthread',
            name='pub_date',
            field=models.DateTimeField(null=True, verbose_name=datetime.datetime(2023, 4, 10, 18, 0, 15, 701255, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='sessionrequest',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
