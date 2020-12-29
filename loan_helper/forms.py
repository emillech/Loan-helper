from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from loan_helper.models import Client


class AddClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'email',
            'address',
            'broker',
            'current_status'
        ]


class UpdateClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'email',
            'marital_status',
            'address',
            'broker',
            'current_status'
        ]


class LoginForm(forms.Form):
    login = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)


class LoanCalculatorForm(forms.Form):
    net_amount = forms.IntegerField()
    bank_charge = forms.FloatField()
    interest_rate = forms.FloatField()
    repayment_term = forms.IntegerField()
    insurance = forms.FloatField()
