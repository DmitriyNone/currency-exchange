# Generated by Django 2.0.4 on 2018-04-23 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('converter', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exchangerate',
            old_name='currency_id',
            new_name='currency',
        ),
        migrations.AddField(
            model_name='exchangerate',
            name='timestamp',
            field=models.IntegerField(default=0),
        ),
    ]
