# Generated by Django 3.0.6 on 2020-06-09 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200608_0203'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordercake',
            name='order_status',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='ordercake',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='ordercake',
            name='special_instructions',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.CreateModel(
            name='OrderProcessing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approval', models.BooleanField(default=False)),
                ('total_amount', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('order_type', models.CharField(choices=[('Pickup', 'Pickup'), ('Delivery', 'Delivery')], default='Pickup', max_length=100)),
                ('address', models.TextField(default='Pickup Order! No Address Supplied')),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.OrderCake')),
            ],
        ),
    ]
