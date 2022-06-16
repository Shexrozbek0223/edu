# Generated by Django 4.0.5 on 2022-06-15 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0003_productionmany'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='production',
            name='product_hs_code',
        ),
        migrations.RemoveField(
            model_name='production',
            name='type_product',
        ),
        migrations.AlterField(
            model_name='production',
            name='product',
            field=models.ManyToManyField(blank=True, to='research.productionmany', verbose_name='Plants+'),
        ),
    ]