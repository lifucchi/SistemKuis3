# Generated by Django 3.1.1 on 2020-11-30 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20201130_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='classes',
            field=models.CharField(blank=True, default=None, max_length=100, verbose_name='kelas'),
        ),
    ]