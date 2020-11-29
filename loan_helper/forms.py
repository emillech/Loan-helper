from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from loan_helper.models import Client, ClientOccupation


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


