# Generated by Django 2.1.5 on 2019-06-28 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_auto_20190628_1808'),
    ]

    operations = [
        migrations.RenameField(
            model_name='practical',
            old_name='things_needed',
            new_name='thingsneeded',
        ),
    ]
