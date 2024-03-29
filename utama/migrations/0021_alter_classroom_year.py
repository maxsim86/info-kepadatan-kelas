# Generated by Django 4.2.7 on 2024-02-28 03:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("utama", "0020_alter_classroom_year"),
    ]

    operations = [
        migrations.AlterField(
            model_name="classroom",
            name="year",
            field=models.CharField(
                choices=[
                    ("PPKI", "PPKI"),
                    ("TAHUNSATU", "TAHUNSATU"),
                    ("TAHUN DUA", "TAHUN DUA"),
                    ("TAHUN TIGA", "TAHUN TIGA"),
                    ("TAHUN EMPAT", "TAHUN EMPAT"),
                    ("TAHUN LIMA", "TAHUN LIMA"),
                    ("TAHUN ENAM", "TAHUN ENAM"),
                ],
                max_length=50,
                verbose_name="tahun kelas",
            ),
        ),
    ]
