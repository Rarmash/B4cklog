# Generated by Django 4.2.4 on 2023-08-10 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('b4cklog', '0004_platform_game_platforms'),
    ]

    operations = [
        migrations.AddField(
            model_name='platform',
            name='abbreviation',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
