# Generated by Django 3.2.7 on 2021-10-06 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0002_cuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reader',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
