# Generated by Django 5.0.4 on 2024-04-07 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unité_de_soins', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dossiermédical',
            options={'ordering': ['chambre'], 'verbose_name_plural': 'Dossier médicaux'},
        ),
        migrations.AlterModelOptions(
            name='personnelsoignant',
            options={'ordering': ['nom', 'prénom'], 'verbose_name_plural': 'Personnel soignant'},
        ),
        migrations.AlterField(
            model_name='dossiermédical',
            name='incontinence',
            field=models.CharField(choices=[('sèche', 'Sèche'), ('humide', 'Humide'), ('<1/2 plein', '<½ plein'), ('>1/2 plein', '>½ plein'), ('changer', 'Changer')], max_length=11),
        ),
    ]
