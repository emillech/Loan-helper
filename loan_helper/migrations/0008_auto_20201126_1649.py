# Generated by Django 3.0.6 on 2020-11-26 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan_helper', '0007_auto_20201125_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='marital_status',
            field=models.IntegerField(choices=[(1, 'Single'), (2, 'Married with DoP'), (3, 'Married without DoP'), (4, 'Widow/Widower'), (5, 'Divorced')]),
        ),
    ]
