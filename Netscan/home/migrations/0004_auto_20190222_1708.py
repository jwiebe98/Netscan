# Generated by Django 2.1.5 on 2019-02-22 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20190222_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='first_ping',
            field=models.DateField(),
        ),
    ]
