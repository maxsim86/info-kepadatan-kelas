# Generated by Django 4.2.7 on 2024-03-14 04:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profilpersonaliti', '0004_rename_choice_userresponse_selected_choice'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='title',
            new_name='text',
        ),
    ]
