# Generated by Django 4.2.11 on 2024-06-22 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programacion', '0010_usuario_is_active_alter_usuario_groups_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='respuestaejercicio',
            name='codigo_archivo',
            field=models.FileField(blank=True, null=True, upload_to='submissions/'),
        ),
    ]
