# Generated by Django 2.0.2 on 2020-11-11 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='hobby',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
