# Generated by Django 5.0.4 on 2024-05-04 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magasin', '0003_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commande',
            name='totalCde',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=10),
        ),
    ]
