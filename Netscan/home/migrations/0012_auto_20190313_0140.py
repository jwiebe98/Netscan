# Generated by Django 2.1.5 on 2019-03-13 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_auto_20190313_0139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='interface',
            field=models.CharField(max_length=20),
        ),
    ]
