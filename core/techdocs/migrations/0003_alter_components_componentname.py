# Generated by Django 4.2.8 on 2024-01-06 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('techdocs', '0002_components_componentprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='components',
            name='componentName',
            field=models.CharField(max_length=255),
        ),
    ]
