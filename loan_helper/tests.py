from unittest.mock import patch
import pytest
from django.test import Client as Django_Client
from loan_helper.models import Client, Broker, Occupation, ClientOccupation, Bank


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
        'broker': broker_to_add,
        'current_status': 1,
    }
    response = django_client.post(
        "/add_client/", client_data)

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