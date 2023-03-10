# Generated by Django 4.1.5 on 2023-02-10 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0003_auction'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='description',
            field=models.CharField(default='Empty description', max_length=1000),
        ),
        migrations.AddField(
            model_name='auction',
            name='title',
            field=models.CharField(default='Empty Title', max_length=500),
        ),
        migrations.AlterField(
            model_name='auction',
            name='first_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='auction',
            name='last_name',
            field=models.CharField(max_length=100),
        ),
    ]
