# Generated by Django 3.2.12 on 2022-06-04 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('System', '0019_rename_photo_photos'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('report_id', models.AutoField(primary_key=True, serialize=False)),
                ('reporter_id', models.IntegerField(default=0)),
                ('article_id', models.IntegerField(default=0)),
                ('report_title', models.CharField(max_length=80)),
                ('report_reason', models.CharField(max_length=200)),
                ('result', models.IntegerField(default=0)),
            ],
        ),
    ]
