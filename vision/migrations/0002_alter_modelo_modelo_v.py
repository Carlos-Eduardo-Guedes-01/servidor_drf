# Generated by Django 4.2.6 on 2023-10-20 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vision', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelo',
            name='modelo_v',
            field=models.FileField(null=True, unique=True, upload_to=''),
        ),
    ]