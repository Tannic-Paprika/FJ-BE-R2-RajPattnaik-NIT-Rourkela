# Generated by Django 5.0.6 on 2024-05-21 05:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main_app", "0004_budgetgoal"),
    ]

    operations = [
        migrations.AddField(
            model_name="expenses",
            name="shared_by",
            field=models.PositiveIntegerField(default=1),
        ),
    ]
