# Generated by Django 4.2.7 on 2023-11-19 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utama', '0011_remove_info_level_tingkatan'),
    ]

    operations = [
        migrations.CreateModel(
            name='TahunLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tahun', models.CharField(choices=[('0', 'Pra Sekolah'), ('1', 'Tahun 1'), ('2', 'Tahun 2'), ('3', 'Tahun 3'), ('4', 'Tahun 4'), ('5', 'Tahun 5')], max_length=1)),
            ],
        ),
    ]