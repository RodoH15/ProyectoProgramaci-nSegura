# Generated by Django 4.2.11 on 2024-06-30 20:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('programacion', '0014_usuario_bot_id_usuario_chat_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='respuestaejercicio',
            name='fecha_subida',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='ejercicio',
            name='casos_de_prueba',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='ejercicio',
            name='fecha_entrega',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='ejercicio',
            name='fecha_inicio',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='ejercicio',
            name='nombre_ejercicio',
            field=models.CharField(max_length=255),
        ),
    ]