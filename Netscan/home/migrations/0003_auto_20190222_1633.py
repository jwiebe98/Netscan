# Generated by Django 2.1.5 on 2019-02-22 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20190210_2210'),
    ]

    operations = [
        migrations.RenameField(
            model_name='device',
            old_name='downtime',
            new_name='down_flag',
        ),
        migrations.AddField(
            model_name='device',
            name='first_ping',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
    ]
