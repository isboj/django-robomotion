# Generated by Django 2.0.5 on 2018-09-18 02:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Motion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motion_name', models.CharField(max_length=100)),
                ('motion_category', models.CharField(max_length=100)),
                ('value_info', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Robot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('robot_name', models.CharField(max_length=100)),
                ('robot_category', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField(blank=True)),
                ('motion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='robocms.Motion')),
            ],
        ),
        migrations.AddField(
            model_name='motion',
            name='robot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='robocms.Robot'),
        ),
    ]