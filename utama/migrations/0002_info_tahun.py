# Generated by Django 4.2.7 on 2023-11-24 01:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('utama', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='tahun',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='utama.tahunmodel', verbose_name='Tahun'),
        ),
    ]
