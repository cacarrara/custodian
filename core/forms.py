# coding: utf-8
from django.forms import ModelForm

from core.models import Account, Receivable, Payable


class AccountsModelForm(ModelForm):
    """
    self.user is added in form object by get_form method of Receivable or
    Payable admin
    """
    def __init__(self, *args, **kwargs):
        super(AccountsModelForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(owner=self.user)


class ReceivableModelForm(AccountsModelForm):
    class Meta:
        model = Receivable


class PayableModelForm(AccountsModelForm):
    class Meta:
        model = Payable