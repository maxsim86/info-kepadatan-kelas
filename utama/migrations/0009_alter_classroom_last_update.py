# Generated by Django 4.2.7 on 2024-01-29 09:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("utama", "0008_alter_classroom_last_update"),
    ]

    operations = [
        migrations.AlterField(
            model_name="classroom",
            name="last_update",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
