# Generated by Django 4.1 on 2022-09-19 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0005_paciente_paciente_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='Paciente_Contrasena',
            field=models.CharField(default='', max_length=40),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='Paciente_Correo',
            field=models.CharField(default='', max_length=40),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='Paciente_Rol',
            field=models.CharField(default='', max_length=40),
        ),
        migrations.AlterField(
            model_name='resultado',
            name='Resultado_Descripcion',
            field=models.CharField(max_length=1000),
        ),
    ]
