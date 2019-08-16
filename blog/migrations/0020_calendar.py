# Generated by Django 2.2.3 on 2019-07-05 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_subject'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.CharField(max_length=200)),
                ('room', models.CharField(max_length=200)),
                ('practical', models.CharField(max_length=200)),
                ('technician', models.CharField(max_length=200)),
                ('teacher', models.CharField(max_length=200)),
                ('sets', models.CharField(max_length=200)),
                ('prints', models.CharField(max_length=200)),
            ],
        ),
    ]
