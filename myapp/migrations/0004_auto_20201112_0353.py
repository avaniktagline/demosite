# Generated by Django 2.0.2 on 2020-11-12 03:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20201111_1211'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='cname',
            new_name='c_name',
        ),
    ]
