# Generated by Django 3.1.1 on 2020-10-26 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_auto_20201012_1925'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiztaker',
            name='specific_competency',
        ),
        migrations.RemoveField(
            model_name='specific_competency',
            name='roll_out',
        ),
        migrations.AddField(
            model_name='base_competency',
            name='roll_out',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='ScoreDetil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(max_length=200)),
                ('quiz_taker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_taker', to='quiz.quiztaker')),
                ('specific_competency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='indikators', to='quiz.specific_competency')),
            ],
        ),
    ]
