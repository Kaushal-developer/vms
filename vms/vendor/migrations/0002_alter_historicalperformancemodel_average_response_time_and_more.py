# Generated by Django 4.2.11 on 2024-04-29 18:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("vendor", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalperformancemodel",
            name="average_response_time",
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name="historicalperformancemodel",
            name="fulfillment_rate",
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name="historicalperformancemodel",
            name="on_time_delivery_rate",
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name="historicalperformancemodel",
            name="quality_rating_avg",
            field=models.FloatField(default=0),
        ),
    ]
