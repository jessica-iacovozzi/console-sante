# Generated by Django 5.0.4 on 2024-04-13 00:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('unité_de_soins', '0006_alter_dossiermédical_options_rendezvous'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rendezvous',
            options={'ordering': ['date', 'durée'], 'verbose_name': 'Rendez-vous', 'verbose_name_plural': 'Rendez-vous'},
        ),
    ]
