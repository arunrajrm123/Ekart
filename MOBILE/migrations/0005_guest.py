# Generated by Django 4.2.1 on 2023-06-23 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MOBILE', '0004_remove_cartitem_product_id_remove_order_product_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('guest_id', models.AutoField(primary_key=True, serialize=False)),
                ('guest_quantity', models.IntegerField()),
                ('guest_variant_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MOBILE.varient')),
            ],
        ),
    ]
