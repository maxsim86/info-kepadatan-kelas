# Generated by Django 4.2.7 on 2023-12-08 03:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("utama", "0012_info_created_info_updated"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tahunmodel",
            name="tahun",
            field=models.CharField(
                choices=[
                    ("PPKI", "PPKI"),
                    ("TAHUN SATU", "TAHUN 1"),
                    ("TAHUN DUA", "TAHUN 2"),
                    ("TAHUN TIGA", "TAHUN 3"),
                    ("TAHUN EMPAT", "TAHUN 4"),
                    ("TAHUN LIMA", "TAHUN 5"),
                    ("TAHUN ENAM", "TAHUN 6"),
                ],
                default="TAHUN 1",
                max_length=11,
                verbose_name="Tingkatan Tahun",
            ),
        ),
    ]