# Generated by Django 5.1.6 on 2025-03-05 19:30

import theatre.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("theatre", "0006_play_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="play",
            name="image",
            field=models.ImageField(
                null=True, upload_to=theatre.models.play_image_path
            ),
        ),
    ]
