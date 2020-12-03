from unittest.mock import patch
import pytest
from django.test import Client as Django_Client
from loan_helper.models import Client, Broker, Occupation, ClientOccupation, Bank, SuccessfulLoan


@pytest.mark.django_db
def test_add_one_client_to_db(django_client, new_broker):
    # sprawdzam ilosc klientow w bazie
    clients_before = Client.objects.count()
    assert clients_before == 0

    # sprawdzam czy objekt broker istnieje
    broker_to_add = Broker.objects.first()
    assert broker_to_add.name == "Company"

    # tworze dane klienta
    client_data = {
        'first_name': 'emil',
        'last_name': 'lech',
        'phone_number': 999,
        'email': 'email@wp.pl',
        'address': 'warsaw',
        'broker': broker_to_add,
        'current_status': 1,
    }

    # dodaje klienta
    response = django_client.post(
        "/add_client/", client_data)

    # tutaj 3 bledy, klient nie istnieje, status_code = 200
    client = Client.objects.get(first_name='emil')
    assert response.status_code == 302
    assert Client.objects.count() == clients_before + 1


@pytest.mark.django_db
def test_add_one_broker_to_db(django_client):
    brokers_before = Broker.objects.count()
    assert brokers_before == 0

    response = django_client.post(
        "/add_broker/", {
            'name': 'Company',
            'phone_number': 666,
            'email': 'email@wp.pl'
        }
    )

    assert response.status_code == 302
    assert Broker.objects.count() == brokers_before + 1
    broker = Broker.objects.get(name='Company')
    assert broker.phone_number == 666
    assert broker.email == 'email@wp.pl'


@pytest.mark.django_db
def test_add_one_bank_to_db(django_client):
    banks_before = Bank.objects.count()
    assert banks_before == 0

    response = django_client.post(
        "/add_bank/", {
            'name': 'New_Bank',
            'address': 'warsaw',
        }
    )

    assert response.status_code == 302
    assert Bank.objects.count() == banks_before + 1
    bank = Bank.objects.get(name="New_Bank")
    assert bank.address == 'warsaw'


@pytest.mark.django_db
def test_add_one_loan_to_db(django_client, new_client, new_broker, new_bank):
    loans_before = SuccessfulLoan.objects.count()
    assert loans_before == 0

    client = Client.objects.first()
    broker = Broker.objects.first()
    bank = Bank.objects.first()

    assert client.first_name == "Emil"
    assert broker.name == "Company"
    assert bank.name == "New Bank"

    loan_data = {
        'client': client,
        'broker': broker,
        'bank': bank,
        'loan_amount_gross': 10000,
        'loan_amount_net': 5000.0,
        'bank_charge': 10.0,
        'interest_rate': 5.0,
        'bank_insurance': 1000.0,
        'repayment_term': 120,
        'instalment_amount': 100.0
    }

    response = django_client.post(
        "/add_loan/", loan_data)

    assert response.status_code == 302
    assert SuccessfulLoan.objects.count() == loans_before + 1
