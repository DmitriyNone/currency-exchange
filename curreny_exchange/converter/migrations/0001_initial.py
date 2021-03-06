# Generated by Django 2.0.4 on 2018-04-23 13:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency_code', models.CharField(choices=[('USD', 'United States Dollars'), ('EUR', 'Euro'), ('CZK', 'Czech Republic Koruna'), ('PLN', 'Polish Zloty')], default='USD', max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='ExchangeRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.DecimalField(decimal_places=10, max_digits=20)),
                ('currency_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='converter.Currency')),
            ],
        ),
    ]
