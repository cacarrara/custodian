# coding: utf-8
from django.forms import ModelForm

from core.models import Account, Receivable, Payable, Person, BusinessSegment


class AccountsModelForm(ModelForm):
    """
    self.user is added in form object by get_form method of Receivable or
    Payable admin
    """
    def __init__(self, *args, **kwargs):
        super(AccountsModelForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(owner=self.user)

    class Meta:
        fields = '__all__'


class ReceivableModelForm(AccountsModelForm):
    """
    self.user is added in form object by get_form method of Receivable or
    Payable admin
    """
    def __init__(self, *args, **kwargs):
        super(ReceivableModelForm, self).__init__(*args, **kwargs)
        self.fields['customer'].queryset = Person.objects.filter(owner=self.user)

    class Meta(AccountsModelForm.Meta):
        model = Receivable


class PayableModelForm(AccountsModelForm):
    """
    self.user is added in form object by get_form method of Receivable or
    Payable admin
    """
    def __init__(self, *args, **kwargs):
        super(PayableModelForm, self).__init__(*args, **kwargs)
        self.fields['supplier'].queryset = Person.objects.filter(owner=self.user)

    class Meta(AccountsModelForm.Meta):
        model = Payable


class PersonModelForm(ModelForm):
    """
    self.user is added in form object by get_form method of Person admin
    """
    def __init__(self, *args, **kwargs):
        super(PersonModelForm, self).__init__(*args, **kwargs)
        self.fields['business_segment'].queryset = BusinessSegment.objects.filter(owner=self.user)

    class Meta:
        model = Person
        fields = '__all__'
