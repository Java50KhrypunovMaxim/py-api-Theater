# Generated by Django 4.1.3 on 2025-03-13 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("theatre", "0008_alter_reservation_created_at_alter_reservation_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticket",
            name="performance",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tickets",
                to="theatre.performance",
            ),
        ),
    ]
