# Generated by Django 2.1.4 on 2018-12-14 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_emailverifyrecord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.CharField(blank=True, default='', help_text='邮箱', max_length=100, verbose_name='邮箱'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='mobile',
            field=models.CharField(blank=True, default='', help_text='电话', max_length=11, verbose_name='电话'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='username',
            field=models.CharField(blank=True, default='', help_text='用户名', max_length=50, verbose_name='用户名'),
        ),
    ]