# Generated by Django 3.2.4 on 2021-07-26 12:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='para',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='일자'),
        ),
    ]
