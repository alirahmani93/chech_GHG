# Generated by Django 3.2.7 on 2021-10-05 03:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_auto_20210917_1917'),
        ('cart', '0009_auto_20211004_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='cart_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='cart_fks', to='cart.cart'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='product_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='product_fks', to='product.product'),
        ),
    ]