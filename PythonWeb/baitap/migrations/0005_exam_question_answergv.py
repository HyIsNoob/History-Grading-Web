# Generated by Django 3.2.6 on 2021-10-06 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baitap', '0004_alter_exam_exam_create'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam_question',
            name='answergv',
            field=models.CharField(blank=True, default='', max_length=700),
        ),
    ]
