# Generated by Django 4.0.5 on 2022-11-15 03:05

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0016_alter_formulario_x_pregunta_formulario_x_pregunta_fechacreacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formulario_x_pregunta',
            name='Formulario_X_Pregunta_FechaCreacion',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 14, 22, 5, 8, 989296)),
        ),
        migrations.AlterField(
            model_name='formulario_x_pregunta',
            name='Resultado_Resultado_Codigo',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='authenticate.resultado'),
            preserve_default=False,
        ),
    ]
