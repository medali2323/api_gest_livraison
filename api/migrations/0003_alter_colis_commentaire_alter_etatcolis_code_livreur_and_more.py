# Generated by Django 4.2.7 on 2023-11-27 08:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_colis_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='colis',
            name='commentaire',
            field=models.TextField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='etatcolis',
            name='code_livreur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.livreur'),
        ),
        migrations.AlterField(
            model_name='etatcolis',
            name='commentaire',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='etatcolis',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
