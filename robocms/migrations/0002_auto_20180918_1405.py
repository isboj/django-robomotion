# Generated by Django 2.0.5 on 2018-09-18 05:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('robocms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='value',
            name='motion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='values', to='robocms.Motion'),
        ),
    ]
