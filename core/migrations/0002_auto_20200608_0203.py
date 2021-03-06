# Generated by Django 3.0.6 on 2020-06-07 20:33

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordercake',
            name='occasion',
        ),
        migrations.AddField(
            model_name='ordercake',
            name='occasion_root',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.UserOccasion'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='useroccasion',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False),
        ),
    ]
