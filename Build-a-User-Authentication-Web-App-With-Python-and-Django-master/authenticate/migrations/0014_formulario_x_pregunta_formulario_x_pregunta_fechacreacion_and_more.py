# Generated by Django 4.0.5 on 2022-11-05 05:51

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0013_alter_formulario_x_pregunta_resultado_resultado_codigo'),
    ]

    operations = [
        migrations.AddField(
            model_name='formulario_x_pregunta',
            name='Formulario_X_Pregunta_FechaCreacion',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 5, 0, 51, 48, 695528)),
        ),
        migrations.AlterField(
            model_name='formulario_x_pregunta',
            name='Resultado_Resultado_Codigo',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='authenticate.resultado'),
        ),
    ]
