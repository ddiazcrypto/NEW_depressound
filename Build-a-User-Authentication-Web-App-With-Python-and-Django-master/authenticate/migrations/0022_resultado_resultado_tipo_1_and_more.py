# Generated by Django 4.1 on 2022-11-15 03:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0021_alter_formulario_x_pregunta_formulario_x_pregunta_fechacreacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultado',
            name='Resultado_tipo_1',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='resultado',
            name='Resultado_tipo_2',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='formulario_x_pregunta',
            name='Formulario_X_Pregunta_FechaCreacion',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 14, 22, 14, 54, 361050)),
        ),
    ]
