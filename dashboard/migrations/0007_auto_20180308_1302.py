# Generated by Django 2.0.1 on 2018-03-08 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_auto_20180307_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refund',
            name='order_date',
            field=models.DateField(blank=True, max_length=50, null=True, verbose_name='거래날짜'),
        ),
        migrations.AlterField(
            model_name='refund',
            name='order_number',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='온라인주문번호'),
            preserve_default=False,
        ),
    ]