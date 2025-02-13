# Generated by Django 5.0.6 on 2024-05-20 08:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main_app", "0002_rename_data_incomesource_date_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="expenses",
            name="date",
            field=models.DateField(
                default=datetime.datetime(
                    2024, 5, 20, 8, 57, 20, 810349, tzinfo=datetime.timezone.utc
                )
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="incomesource",
            name="description",
            field=models.CharField(max_length=255),
        ),
    ]
