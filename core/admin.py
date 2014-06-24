# coding: utf-8
import datetime
from django.contrib import admin

from core.models import (Account, BusinessSegment, Person, 
                        Receivable, Payable, Revenue, Expense)
from core.forms import ReceivableModelForm, PayableModelForm, PersonModelForm


def get_next_month(due_date):
    new_year = due_date.year
    new_month = due_date.month
    new_day = due_date.day

    if new_month == 12:
        new_month = 1
        new_year = due_date.year + 1
    else:
        new_month = due_date.month + 1

    new_due_date = None
    try:
        new_due_date = datetime.date(new_year,new_month,new_day)
    except ValueError:
        new_due_date = datetime.date(new_year,new_month,new_day - 1)

    return new_due_date


class AccountAdmin(admin.ModelAdmin):
    exclude = ('owner', )
    list_display = ('name', 'balance', 'creation_date', )
    readonly_fields = ('balance', )
    search_fields = ('name', )

    def save_model(self, request, obj, form, change):
        """
        Checks if object has no attribute owner (so is a insert operation,
        because it is excluded from admin form) to set current 
        user as owner and initial balance to current balance
        """
        if not hasattr(obj, 'owner'):
            obj.owner = request.user
            obj.balance = obj.init_balance
        obj.save()

    def get_readonly_fields(self, request, obj=None):
        """
        Verifies if is a update (obj != None) operation to set
        init_balance as readonly
        """
        if obj:
            return self.readonly_fields + ('init_balance',)
        else:
            return self.readonly_fields

    def get_queryset(self, request):
        qs = super(AccountAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)


class PersonAdmin(admin.ModelAdmin):
    form = PersonModelForm
    exclude = ('owner', )
    list_display = ('name', 'document', 'city', 'business_segment')
    search_fields = ('name', 'document', 'city', 'business_segment__name')

    def save_model(self, request, obj, form, change):
        """
        Checks if object has no attribute owner (so is a insert operation,
        because it is excluded from admin form) to set current user as owner
        """
        if not hasattr(obj, 'owner'):
            obj.owner = request.user
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        self.form.user = request.user
        return super(PersonAdmin, self).get_form(request, **kwargs)

    def get_queryset(self, request):
        qs = super(PersonAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)


class ReceivableAdmin(admin.ModelAdmin):
    form = ReceivableModelForm
    list_display = ('customer', 'value', 'due_date',
                    'description', 'account')
    search_fields = ('customer__name', 'description', 'account__name')
    actions = ('repeat_next_month',)

    def get_form(self, request, obj=None, **kwargs):
        if obj != None and obj.is_past_due():
            self.exclude = ('due_date', )

        self.form.user = request.user
        return super(ReceivableAdmin, self).get_form(request, **kwargs)

    def repeat_next_month(self, request, queryset):
        for receivable in queryset:
            new_due_date = get_next_month(receivable.due_date)
            new_payable = Receivable.objects.create(
                            value=receivable.value,
                            due_date=new_due_date,
                            description=receivable.description,
                            account=receivable.account,
                            customer=receivable.customer
                        )

            new_payable.save()

    def get_queryset(self, request):
        qs = super(ReceivableAdmin, self).get_queryset(request)
        return qs.filter(account__owner=request.user)


class PayableAdmin(admin.ModelAdmin):
    form = PayableModelForm
    list_display = ('supplier', 'value', 'due_date',
                    'description', 'account')
    search_fields = ('supplier__name', 'description', 'account__name')
    actions = ('repeat_next_month',)

    def get_form(self, request, obj=None, **kwargs):
        if obj != None and obj.is_past_due():
            self.exclude = ('due_date', )

        self.form.user = request.user
        return super(PayableAdmin, self).get_form(request, **kwargs)

    def repeat_next_month(self, request, queryset):
        for payable in queryset:
            new_due_date = get_next_month(payable.due_date)
            new_payable = Payable.objects.create(
                            value=payable.value,
                            due_date=new_due_date,
                            description=payable.description,
                            account=payable.account,
                            supplier=payable.supplier
                        )
            new_payable.save()

    def get_queryset(self, request):
        qs = super(PayableAdmin, self).get_queryset(request)
        return qs.filter(account__owner=request.user)


class RevenueAdmin(admin.ModelAdmin):
    list_display = ('value', 'date', 'customer', 'account')
    search_fields = ('account__name', 'customer__name')
    list_filter = ('date', 'account',)


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('value', 'date', 'supplier', 'account')
    search_fields = ('account__name', 'supplier__name')
    list_filter = ('date', 'account',)


class BusinessSegmentAdmin(admin.ModelAdmin):
    exclude = ('owner', )
    search_fields = ('name', )

    def save_model(self, request, obj, form, change):
        """
        Checks if object has no attribute owner (so is a insert operation,
        because it is excluded from admin form) to set current user as owner
        """
        if not hasattr(obj, 'owner'):
            obj.owner = request.user
        obj.save()

    def get_queryset(self, request):
        qs = super(BusinessSegmentAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)


admin.site.register(Account, AccountAdmin)
admin.site.register(BusinessSegment, BusinessSegmentAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Receivable, ReceivableAdmin)
admin.site.register(Payable, PayableAdmin)
admin.site.register(Revenue, RevenueAdmin)
admin.site.register(Expense, ExpenseAdmin)