# coding: utf-8
from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now as dj_timezone_now


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

    def withdraw(self, amount=0.0):
        self.balance -= amount
        self.save()

    def deposit(self, amount=0.0):
        self.balance += amount
        self.save()


class Accounts(models.Model):
    value = models.DecimalField(max_digits=13, decimal_places=2, default=Decimal('0.00'), verbose_name='Value')
    due_date = models.DateField(verbose_name='Due Date')
    description = models.CharField(max_length=256, verbose_name='Description')

    def is_past_due(self):
        return self.due_date > date.today()

    class Meta:
        abstract = True
        ordering = ['due_date']


@python_2_unicode_compatible
class BusinessSegment(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name='Name')
    owner = models.ForeignKey(User, related_name="business_segments", verbose_name="Owner")

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
    owner = models.ForeignKey(User, related_name="persons", verbose_name="Owner")

    def __str__(self):
        if self.document:
            return "%s (%s)" % (self.name, self.document)
        else:
            return self.name


class Transaction(models.Model):
    date = models.DateField(default=dj_timezone_now, verbose_name='Date')
    value = models.DecimalField(max_digits=13, decimal_places=2, verbose_name='Value')

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Revenue(Transaction):
    account = models.ForeignKey(Account, related_name='related_revenues', verbose_name='Related Account')
    customer = models.ForeignKey(Person, related_name='revenues', verbose_name='Customer')

    def __str__(self):
        return '%s - %s' % (self.value, self.customer.name)

    def save(self):
        super(Revenue, self).save()
        self.account.deposit(amount=self.value)


@python_2_unicode_compatible
class Expense(Transaction):
    account = models.ForeignKey(Account, related_name='related_expenses', verbose_name='Related Account')
    supplier = models.ForeignKey(Person, related_name='expenses', verbose_name='Supplier')

    def __str__(self):
        return '%s - %s' % (self.value, self.supplier.name)

    def save(self):
        super(Expense, self).save()
        self.account.withdraw(amount=self.value)


class TransactionEvent(models.Model):
    TRANSACTION_TYPES = (
        ('E', 'Expense'),
        ('R', 'Revenue'),
    )
    account = models.ForeignKey(Account, related_name='related_transaction_events', verbose_name='Related Account')
    date = models.DateField(auto_now_add=True, verbose_name='Date')
    value = models.DecimalField(max_digits=13, decimal_places=2, verbose_name='Value')
    transaction_type = models.CharField(max_length=1, choices=TRANSACTION_TYPES)


@python_2_unicode_compatible
class Receivable(Accounts):
    account = models.ForeignKey(Account, related_name='related_receivables', verbose_name='Related Account')
    customer = models.ForeignKey(Person, related_name='receivables', verbose_name='Customer')
    received = models.BooleanField(default=False, verbose_name='Received')

    def __str__(self):
        return '%s: %s - %s' % (self.due_date, self.value, self.customer.name)


@python_2_unicode_compatible
class Payable(Accounts):
    account = models.ForeignKey(Account, related_name='related_payables', verbose_name='Related Account')
    supplier = models.ForeignKey(Person, related_name='payables', verbose_name='Supplier')
    paid = models.BooleanField(default=False, verbose_name='Paid')

    def __str__(self):
        return '%s: %s - %s' % (self.due_date, self.value, self.supplier.name)


@receiver(post_save, sender=Revenue)
@receiver(post_save, sender=Expense)
def post_save_transaction_event(sender, **kwargs):
    transaction_type = None
    if sender == Revenue:
        transaction_type = 'R'
    elif sender == Expense:
        transaction_type = 'E'

    transaction = kwargs['instance']
    transaction_event = TransactionEvent.objects.create(
        value=transaction.value,
        transaction_type=transaction_type,
        account=transaction.account
    )
    transaction_event.save()
