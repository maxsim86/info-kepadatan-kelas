# Generated by Django 4.2.7 on 2023-11-24 03:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utama', '0005_alter_info_options_alter_listsekolah_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tahunmodel',
            options={'ordering': ['tahun'], 'verbose_name': 'Tahun', 'verbose_name_plural': 'Tahun'},
        ),
    ]
