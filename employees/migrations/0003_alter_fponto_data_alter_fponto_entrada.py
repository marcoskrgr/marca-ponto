# Generated by Django 5.0.3 on 2024-03-30 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0002_alter_fponto_idcolaborador'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fponto',
            name='data',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='fponto',
            name='entrada',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
