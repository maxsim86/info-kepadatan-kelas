# Generated by Django 4.2.7 on 2024-04-01 05:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "profilpersonaliti",
            "0002_remove_quiz_an_remove_quiz_as_question_an_and_more",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="question",
            old_name="AN",
            new_name="question_number",
        ),
        migrations.RemoveField(
            model_name="question",
            name="AS",
        ),
    ]