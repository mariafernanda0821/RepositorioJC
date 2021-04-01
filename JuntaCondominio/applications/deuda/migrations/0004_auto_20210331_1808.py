# Generated by Django 3.1.6 on 2021-03-31 18:08

from django.db import migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('deuda', '0003_auto_20210331_0025'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registrodeudas',
            old_name='deuda',
            new_name='deuda_pagar',
        ),
        migrations.RemoveField(
            model_name='registrodeudas',
            name='deudas_total',
        ),
        migrations.AddField(
            model_name='referenciapago',
            name='created',
            field=model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created'),
        ),
        migrations.AddField(
            model_name='referenciapago',
            name='modified',
            field=model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified'),
        ),
    ]