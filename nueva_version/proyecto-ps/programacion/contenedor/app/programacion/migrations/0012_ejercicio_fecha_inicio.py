# Generated by Django 4.2.11 on 2024-06-25 18:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('programacion', '0011_respuestaejercicio_codigo_archivo'),
    ]

    operations = [
        migrations.AddField(
            model_name='ejercicio',
            name='fecha_inicio',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]