# Generated by Django 4.2.1 on 2024-05-20 09:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Salt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('density', models.FloatField(help_text='Плотность раствора (г/см³)')),
                ('salt_consumption', models.FloatField(help_text='Расход соли (кг/м³)')),
                ('water_consumption', models.FloatField(help_text='Расход пресной воды (л/м³)')),
                ('salt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solutions', to='calculator.salt')),
            ],
        ),
    ]
