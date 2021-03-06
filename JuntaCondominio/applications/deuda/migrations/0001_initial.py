# Generated by Django 3.1.6 on 2021-04-26 20:05

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('edificio', '0001_initial'),
        ('administracion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistroDeudas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('deuda_ocumulada', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Deuda Acumulada')),
                ('deuda_pagar', models.DecimalField(decimal_places=2, default=0, max_digits=20, null=True, verbose_name='Deuda Pagar')),
                ('apartamento', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='edificio.apartamento', verbose_name='Apartamento')),
            ],
            options={
                'verbose_name': 'Registro Deuda',
                'verbose_name_plural': 'Registro Deudas',
                'ordering': ['apartamento'],
            },
        ),
        migrations.CreateModel(
            name='ReferenciaPago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('tipo_pago', models.CharField(blank=True, choices=[('Transferencia', 'Transferencia'), ('Efectivo BS', 'Efectivo BS'), ('Divisa', 'Divisa'), ('Deposito', 'Depositos')], max_length=50, verbose_name='Tipo de pago')),
                ('monto_pagar', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Monto de Pago')),
                ('referencia_pago', models.CharField(blank=True, max_length=50, verbose_name='Referencia de Pago')),
                ('descripcion', models.TextField(blank=True, verbose_name='Descripcion')),
                ('pago_bool', models.BooleanField(default=False, verbose_name='Pago')),
                ('reporte', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='administracion.reporte', verbose_name='Reporte')),
            ],
            options={
                'verbose_name': 'Referencia Pago',
                'verbose_name_plural': 'Referencia Pagos',
            },
        ),
    ]
