# Generated by Django 4.1.7 on 2023-04-03 20:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_merge_20230403_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussionreplies',
            name='reply_date',
            field=models.DateTimeField(null=True, verbose_name=datetime.datetime(2023, 4, 3, 20, 31, 21, 253795, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='discussionthread',
            name='pub_date',
            field=models.DateTimeField(null=True, verbose_name=datetime.datetime(2023, 4, 3, 20, 31, 21, 253500, tzinfo=datetime.timezone.utc)),
        ),
    ]