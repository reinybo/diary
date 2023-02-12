# Generated by Django 4.1.5 on 2023-02-11 21:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_entry_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=200)),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.entry')),
            ],
        ),
    ]
