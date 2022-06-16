# Generated by Django 4.0.5 on 2022-06-15 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductionMany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_hs_code', models.CharField(blank=True, max_length=15, null=True, verbose_name='KOD TN ved')),
                ('product', models.ManyToManyField(blank=True, to='research.plants', verbose_name='Plants+')),
                ('type_product', models.ManyToManyField(blank=True, related_name='Product types+', to='research.producttypes')),
            ],
        ),
    ]
