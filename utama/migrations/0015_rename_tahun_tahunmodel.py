# Generated by Django 4.2.7 on 2023-11-19 06:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utama', '0014_tahun_remove_info_tahun'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Tahun',
            new_name='TahunModel',
        ),
    ]