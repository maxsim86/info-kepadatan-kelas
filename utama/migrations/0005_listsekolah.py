# Generated by Django 4.2.7 on 2023-11-17 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utama', '0004_info_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListSekolah',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
    ]