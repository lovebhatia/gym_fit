# Generated by Django 5.0.2 on 2024-03-13 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_bmirecord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bmirecord',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
