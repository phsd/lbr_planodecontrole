# Generated by Django 2.1.10 on 2019-07-08 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='headerPlanoControle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mo', models.CharField(max_length=50)),
                ('seriei', models.IntegerField(db_index=True)),
                ('serieii', models.IntegerField(db_index=True)),
                ('serieiii', models.IntegerField(db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='inspecaoPlanoControle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serie', models.IntegerField(db_index=True)),
                ('valor', models.CharField(max_length=50)),
                ('id_usuario', models.IntegerField()),
                ('dataRegistro', models.DateTimeField(auto_now_add=True)),
                ('id_HPC', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='telaPrincipal.headerPlanoControle')),
            ],
        ),
        migrations.CreateModel(
            name='itemInspecaoPC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField(db_index=True)),
                ('cor', models.CharField(max_length=50)),
                ('requisito', models.CharField(max_length=50)),
                ('ilustracao', models.CharField(max_length=50)),
                ('metodoinstrucao', models.CharField(max_length=50)),
                ('unidade', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='inspecaoplanocontrole',
            name='id_itemInspecaoPC',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='telaPrincipal.itemInspecaoPC'),
        ),
    ]
