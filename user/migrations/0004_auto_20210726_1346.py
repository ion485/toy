# Generated by Django 3.2.4 on 2021-07-26 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_rename_permission_user_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='권한'),
        ),
        migrations.AlterField(
            model_name='user',
            name='location',
            field=models.CharField(default=False, max_length=30, verbose_name='장소'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, max_length=30, verbose_name='이름'),
        ),
    ]
