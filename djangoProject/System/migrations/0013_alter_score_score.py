# Generated by Django 4.0.4 on 2022-06-03 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('System', '0012_remove_score_id_score_score_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='score',
            field=models.DecimalField(decimal_places=1, max_digits=2),
        ),
    ]
