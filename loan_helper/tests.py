from unittest.mock import patch
import pytest
from django.test import Client as Django_Client
from loan_helper.models import Client, Broker, Occupation, ClientOccupation, Bank, SuccessfulLoan


@pytest.mark.django_db
def test_add_one_client_to_db(django_client, new_broker):
    clients_before = Client.objects.count()
    assert clients_before == 0

    broker_to_add = Broker.objects.first()
    assert broker_to_add.name == "Company"

    client_data = {
        'first_name': 'emil',
        'last_name': 'lech',
        'phone_number': 999,
        'email': 'email@wp.pl',
        'address': 'warsaw',
        'broker': broker_to_add.id,
        'current_status': 1,
    }

    response = django_client.post(
        "/add_client/", client_data)

    client = Client.objects.get(first_name='emil')
    assert client.last_name == 'lech'
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
        'client': client.id,
        'broker': broker.id,
        'bank': bank.id,
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


@pytest.mark.django_db
def test_show_clients_list(django_client, new_client):
    response = django_client.get("/all_clients/", {})

    assert response.status_code == 200
    client = Client.objects.get(first_name='Emil')
    assert client in response.context['client_list']


@pytest.mark.django_db
def test_show_brokers_list(django_client, new_broker):
    response = django_client.get("/all_brokers/", {})

    assert response.status_code == 200
    broker = Broker.objects.get(name="Company")
    assert broker in response.context['broker_list']


@pytest.mark.django_db
def test_show_banks_list(django_client, new_bank):
    response = django_client.get("/all_banks/", {})

    assert response.status_code == 200
    bank = Bank.objects.get(name="New Bank")
    assert bank in response.context['bank_list']


@pytest.mark.django_db
def test_show_loans_list(django_client, new_loan):
    response = django_client.get("/all_loans/", {})

    assert response.status_code == 200
    loan = SuccessfulLoan.objects.get(loan_amount_gross=10000)
    assert loan in response.context['successfulloan_list']


@pytest.mark.django_db
def test_show_client_details(django_client, new_client):
    client = Client.objects.get(first_name="Emil")
    assert Client.objects.count() == 1

    response = django_client.get(f"/client_details/{client.id}/", {})
    
    assert response.status_code == 200
    assert 'Emil' in str(response.context['client'])
