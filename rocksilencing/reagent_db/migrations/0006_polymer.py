# Generated by Django 5.1.2 on 2024-12-22 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reagent_db", "0005_weightingagent"),
    ]

    operations = [
        migrations.CreateModel(
            name="Polymer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Название")),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("Водорастворимый полимер", "Водорастворимый полимер"),
                            ("Природный полимер", "Природный полимер"),
                            ("Биополимер", "Биополимер"),
                            ("Синтетический полимер", "Синтетический полимер"),
                        ],
                        max_length=100,
                        verbose_name="Тип полимера",
                    ),
                ),
                ("application", models.TextField(verbose_name="Применение")),
            ],
            options={
                "verbose_name": "Полимер",
                "verbose_name_plural": "Полимеры",
            },
        ),
    ]
