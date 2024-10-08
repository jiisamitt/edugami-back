# Generated by Django 4.2.7 on 2024-10-02 22:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0002_answer'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests', to='interview.student')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='interview.test')),
            ],
            options={
                'unique_together': {('student', 'test')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='answer',
            name='student_test',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='interview.studenttest'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together={('student_test', 'question')},
        ),
        migrations.RemoveField(
            model_name='answer',
            name='student',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='test',
        ),
    ]
