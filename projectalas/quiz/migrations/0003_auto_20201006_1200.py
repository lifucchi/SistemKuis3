# Generated by Django 3.1.1 on 2020-10-06 05:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_remove_question_c_prob'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='discrimination_b',
            new_name='discrimination',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='level_a',
            new_name='level',
        ),
    ]
