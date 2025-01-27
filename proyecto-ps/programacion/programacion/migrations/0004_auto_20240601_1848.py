# Generated by Django 2.2.28 on 2024-06-01 18:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('programacion', '0003_failedloginattempt'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ejercicio',
            old_name='titulo',
            new_name='nombre_ejercicio',
        ),
        migrations.RemoveField(
            model_name='ejercicio',
            name='descripcion',
        ),
        migrations.RemoveField(
            model_name='ejercicio',
            name='fecha_subida',
        ),
        migrations.RemoveField(
            model_name='ejercicio',
            name='usuario',
        ),
        migrations.AddField(
            model_name='ejercicio',
            name='fecha_entrega',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='ejercicio',
            name='nombre_alumno',
            field=models.CharField(default='Alumno', max_length=100),
        ),
    ]
