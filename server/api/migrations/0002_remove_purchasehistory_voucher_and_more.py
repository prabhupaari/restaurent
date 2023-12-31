# Generated by Django 5.0 on 2023-12-20 06:34

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchasehistory',
            name='voucher',
        ),
        migrations.AddField(
            model_name='purchasehistory',
            name='bill_amount',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='CustomerVoucher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_used', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.customer')),
                ('voucher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.voucher')),
            ],
        ),
        migrations.AddField(
            model_name='purchasehistory',
            name='used_voucher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.customervoucher'),
        ),
    ]
