# conding: utf-8
from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Account(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name='Name')
    init_balance = models.DecimalField(max_digits=13, decimal_places=2, 
                                    default=Decimal('0.00'), verbose_name='Initial Balance')
    balance = models.DecimalField(max_digits=13, decimal_places=2, 
                                    default=Decimal('0.00'), verbose_name='Balance')
    creation_date = models.DateField(auto_now_add=True, verbose_name='Creation Date')
    owner = models.ForeignKey(User, related_name='accounts', verbose_name='Owner')
    
    class Meta:
        ordering = ['-creation_date']

    def __str__(self):
        return "%s (%s)" % (self.name, self.balance)


class Accounts(models.Model):
    value = models.DecimalField(max_digits=13, decimal_places=2, default=Decimal('0.00'), verbose_name='Value')
    due_date = models.DateField(verbose_name='Due Date')
    description = models.CharField(max_length=256, verbose_name='Description')

    class Meta:
        abstract = True
        ordering = ['due_date']


@python_2_unicode_compatible
class BusinessSegment(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name='Name')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Person(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name='Name')
    document = models.CharField(max_length=128, blank=True, null=True, verbose_name='Document')
    phone_number = models.CharField(max_length=128, blank=True, null=True, verbose_name='Phone Nr.')
    address = models.CharField(max_length=256, blank=True, null=True, verbose_name='Address')
    city = models.CharField(max_length=128, verbose_name='City')
    state = models.CharField(max_length=128, verbose_name='State')
    country = models.CharField(max_length=128, verbose_name='Country')
    business_segment = models.ForeignKey(BusinessSegment, verbose_name='Business Segment')

    def __str__(self):
        if self.document:
            return "%s (%s)" % (self.name, self.document)
        else:
            return self.name


class Transaction(models.Model):
    date = models.DateField(auto_now_add=True, verbose_name='Date')
    value = models.DecimalField(max_digits=13, decimal_places=2, verbose_name='Value')

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Revenue(Transaction):
    account = models.ForeignKey(Account, related_name='related_revenues', verbose_name='Related Account')
    customer = models.ForeignKey(Person, related_name='revenues', verbose_name='Customer')

    def __str__(self):
        return '%s - %s' % (self.value, self.customer.name)


@python_2_unicode_compatible
class Expense(Transaction):
    account = models.ForeignKey(Account, related_name='related_expenses', verbose_name='Related Account')
    supplier = models.ForeignKey(Person, related_name='expenses', verbose_name='Supplier')

    def __str__(self):
        return '%s - %s' % (self.value, self.supplier.name)


class TransactionEvent(models.Model):
    TRANSACTION_TYPES = (
        ('E', 'Expense'),
        ('R', 'Revenue'),
    )
    date = models.DateField(auto_now_add=True, verbose_name='Date')
    value = models.DecimalField(max_digits=13, decimal_places=2, verbose_name='Value')
    transaction_type = models.CharField(max_length=1, choices=TRANSACTION_TYPES)


@python_2_unicode_compatible
class Receivable(Accounts):
    account = models.ForeignKey(Account, related_name='related_receivables', verbose_name='Related Account')
    customer = models.ForeignKey(Person, related_name='receivables', verbose_name='Customer')

    def __str__(self):
        return '%s: %s - %s' % (self.due_date, self.value, self.customer.name)


@python_2_unicode_compatible
class Payable(Accounts):
    account = models.ForeignKey(Account, related_name='related_payables', verbose_name='Related Account')
    supplier = models.ForeignKey(Person, related_name='payables', verbose_name='Supplier')

    def __str__(self):
        return '%s: %s - %s' % (self.due_date, self.value, self.supplier.name)
