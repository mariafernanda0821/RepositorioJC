# Generated by Django 3.1.6 on 2021-03-29 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edificio', '0002_auto_20210329_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartamento',
            name='torre',
            field=models.CharField(choices=[('1', 'Torre A'), ('2', 'Torre B'), ('3', 'Alquiles')], max_length=1, verbose_name='Torres'),
        ),
    ]