# Generated by Django 3.0.6 on 2020-06-09 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20200610_0101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordercake',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AlterField(
            model_name='orderprocessing',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AlterField(
            model_name='orderprocessing',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
    ]