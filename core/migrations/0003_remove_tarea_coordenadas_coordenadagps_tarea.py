# Generated by Django 4.1 on 2023-11-04 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_drone_fotografia'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tarea',
            name='coordenadas',
        ),
        migrations.AddField(
            model_name='coordenadagps',
            name='tarea',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.tarea'),
        ),
    ]