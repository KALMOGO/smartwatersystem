# Generated by Django 4.2.13 on 2024-06-09 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainApp", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="useriot",
            name="water_name",
            field=models.CharField(default=1, max_length=250),
            preserve_default=False,
        ),
    ]
