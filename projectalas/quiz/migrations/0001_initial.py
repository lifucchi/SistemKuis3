# Generated by Django 3.1.1 on 2020-10-12 12:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=200)),
                ('is_correct', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Base_Competency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('ability', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=200)),
                ('level', models.FloatField(default=0)),
                ('discrimination', models.FloatField(default=0)),
                ('order', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='QuizTaker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('completed', models.BooleanField(default=False)),
                ('date_finished', models.DateTimeField(null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('recommendation', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('slug', models.SlugField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='UsersAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('grade', models.IntegerField(default=0)),
                ('answer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='quiz.answer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='quiz.question')),
                ('quiztaker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_answers', to='quiz.quiztaker')),
            ],
        ),
        migrations.CreateModel(
            name='Specific_Competency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('description', models.CharField(max_length=70)),
                ('order', models.IntegerField(default=0)),
                ('roll_out', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('base_Competency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='k_dasar', to='quiz.base_competency')),
            ],
            options={
                'verbose_name_plural': 'Specific_Competencies',
                'ordering': ['timestamp'],
            },
        ),
        migrations.AddField(
            model_name='quiztaker',
            name='specific_competency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='indikator_diambil', to='quiz.specific_competency'),
        ),
        migrations.AddField(
            model_name='quiztaker',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='murid', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='QuizLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ql_p', models.FloatField(default=0)),
                ('ql_c', models.FloatField(default=0)),
                ('ql_r', models.FloatField(default=0)),
                ('ql_ability', models.FloatField(default=0)),
                ('ql_deltaability', models.FloatField(default=0)),
                ('quiztaker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='person_answers', to='quiz.quiztaker')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='specific_Competency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='indikator', to='quiz.specific_competency'),
        ),
        migrations.CreateModel(
            name='Core_Competency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('desc', models.CharField(max_length=100)),
                ('classes', models.CharField(max_length=100)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mapel', to='quiz.subject')),
            ],
        ),
        migrations.AddField(
            model_name='base_competency',
            name='core_Competency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='k_inti', to='quiz.core_competency'),
        ),
        migrations.AddField(
            model_name='base_competency',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topictopic', to='quiz.topic'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='quiz.question'),
        ),
    ]
