# Generated by Django 4.2.8 on 2024-01-07 18:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('techdocs', '0005_alter_components_options_alter_machineissues_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='machineissues',
            name='fixTime',
        ),
    ]