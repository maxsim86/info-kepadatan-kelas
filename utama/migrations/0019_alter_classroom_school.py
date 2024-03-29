# Generated by Django 4.2.7 on 2024-02-27 02:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("utama", "0018_alter_classroom_average_alter_classroom_school_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="classroom",
            name="school",
            field=models.CharField(
                choices=[
                    ("SK KLANG", "SK KLANG"),
                    ("SK TELOK GADONG", "SK TELOK GADONG"),
                    ("SK PELABUHAN KLANG", "SK PELABUHAN KLANG"),
                    ("SK TELOK MENEGON", "SK TELOK MENEGON"),
                    ("SK BUKIT NAGA ", "SK BUKIT NAGA"),
                    ("SK JALAN KEBUN", "SK JALAN KEBUN"),
                    ("SK BATU BELAH", "SK BATU BELAH"),
                ],
                max_length=50,
                verbose_name="Pilihan Sekolah",
            ),
        ),
    ]
