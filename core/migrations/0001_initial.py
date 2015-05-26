# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Name')),
                ('init_balance', models.DecimalField(default=Decimal('0.00'), decimal_places=2, verbose_name='Initial Balance', max_digits=13)),
                ('balance', models.DecimalField(default=Decimal('0.00'), decimal_places=2, verbose_name='Balance', max_digits=13)),
                ('creation_date', models.DateField(auto_now_add=True, verbose_name='Creation Date')),
                ('owner', models.ForeignKey(related_name='accounts', to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'ordering': ['-creation_date'],
            },
        ),
        migrations.CreateModel(
            name='BusinessSegment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Name')),
                ('owner', models.ForeignKey(related_name='business_segments', to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Date')),
                ('value', models.DecimalField(decimal_places=2, verbose_name='Value', max_digits=13)),
                ('account', models.ForeignKey(related_name='related_expenses', to='core.Account', verbose_name='Related Account')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Payable',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('value', models.DecimalField(default=Decimal('0.00'), decimal_places=2, verbose_name='Value', max_digits=13)),
                ('due_date', models.DateField(verbose_name='Due Date')),
                ('description', models.CharField(max_length=256, verbose_name='Description')),
                ('paid', models.BooleanField(default=False, verbose_name='Paid')),
                ('account', models.ForeignKey(related_name='related_payables', to='core.Account', verbose_name='Related Account')),
            ],
            options={
                'abstract': False,
                'ordering': ['due_date'],
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Name')),
                ('document', models.CharField(max_length=128, null=True, verbose_name='Document', blank=True)),
                ('phone_number', models.CharField(max_length=128, null=True, verbose_name='Phone Nr.', blank=True)),
                ('address', models.CharField(max_length=256, null=True, verbose_name='Address', blank=True)),
                ('city', models.CharField(max_length=128, verbose_name='City')),
                ('state', models.CharField(max_length=128, verbose_name='State')),
                ('country', models.CharField(max_length=128, verbose_name='Country')),
                ('business_segment', models.ForeignKey(to='core.BusinessSegment', verbose_name='Business Segment')),
                ('owner', models.ForeignKey(related_name='persons', to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
        ),
        migrations.CreateModel(
            name='Receivable',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('value', models.DecimalField(default=Decimal('0.00'), decimal_places=2, verbose_name='Value', max_digits=13)),
                ('due_date', models.DateField(verbose_name='Due Date')),
                ('description', models.CharField(max_length=256, verbose_name='Description')),
                ('received', models.BooleanField(default=False, verbose_name='Received')),
                ('account', models.ForeignKey(related_name='related_receivables', to='core.Account', verbose_name='Related Account')),
                ('customer', models.ForeignKey(related_name='receivables', to='core.Person', verbose_name='Customer')),
            ],
            options={
                'abstract': False,
                'ordering': ['due_date'],
            },
        ),
        migrations.CreateModel(
            name='Revenue',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Date')),
                ('value', models.DecimalField(decimal_places=2, verbose_name='Value', max_digits=13)),
                ('account', models.ForeignKey(related_name='related_revenues', to='core.Account', verbose_name='Related Account')),
                ('customer', models.ForeignKey(related_name='revenues', to='core.Person', verbose_name='Customer')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TransactionEvent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('date', models.DateField(auto_now_add=True, verbose_name='Date')),
                ('value', models.DecimalField(decimal_places=2, verbose_name='Value', max_digits=13)),
                ('transaction_type', models.CharField(max_length=1, choices=[('E', 'Expense'), ('R', 'Revenue')])),
                ('account', models.ForeignKey(related_name='related_transaction_events', to='core.Account', verbose_name='Related Account')),
            ],
        ),
        migrations.AddField(
            model_name='payable',
            name='supplier',
            field=models.ForeignKey(related_name='payables', to='core.Person', verbose_name='Supplier'),
        ),
        migrations.AddField(
            model_name='expense',
            name='supplier',
            field=models.ForeignKey(related_name='expenses', to='core.Person', verbose_name='Supplier'),
        ),
    ]
