# Generated by Django 4.2.4 on 2023-08-30 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Webhook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('event', models.CharField(max_length=100)),
                ('version', models.IntegerField()),
                ('rule', models.CharField(max_length=200)),
                ('url', models.URLField()),
                ('security_strategy', models.CharField(max_length=50)),
                ('secret', models.CharField(max_length=100)),
            ],
        ),
    ]
