# Generated by Django 4.1.3 on 2025-02-28 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("theatre", "0002_rename_actor_play_actors_alter_play_genre"),
    ]

    operations = [
        migrations.RenameField(
            model_name="play",
            old_name="genre",
            new_name="genres",
        ),
    ]
