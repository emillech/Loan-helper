import pytest
from django.test import Client as Django_Client
from loan_helper.models import Client, Broker, Occupation, ClientOccupation, Bank, SuccessfulLoan
from faker import Faker
import random


fake = Faker()


@pytest.fixture
def django_client():
    django_client = Django_Client()
    return django_client


@pytest.fixture
def new_bank():
    new_bank = Bank.objects.create(
            name="New Bank",
            address="warsaw"
        )
    return new_bank


@pytest.fixture
def new_broker():
    new_broker = Broker.objects.create(
            name="Company",
            phone_number=random.randint(100000000, 999999999),
            email=fake.email()
        )
    return new_broker


@pytest.fixture
def new_occupation():
    random_number = random.randint(1, 4)
    new_occupation = Occupation.objects.create(occupation=random_number)
    return new_occupation


@pytest.fixture
def new_client(new_broker, new_occupation):
    one_broker = new_broker
    phone_number = random.randint(100000000, 999999999)
    current_status = random.randint(1, 7)
    one_client = Client.objects.create(
        first_name="Emil",
        last_name=fake.last_name(),
        phone_number=phone_number,
        email=fake.email(),
        address=fake.address(),
        broker=one_broker,
        current_status=current_status,
    )

    return one_client


@pytest.fixture
def new_loan(new_client, new_broker, new_bank):
    client = Client.objects.first()
    broker = Broker.objects.first()
    bank = Bank.objects.first()

    loan = SuccessfulLoan.objects.create(
        client=client,
        broker=broker,
        bank=bank,
        loan_amount_gross=10000,
        loan_amount_net=5000.0,
        bank_charge=10.0,
        interest_rate=5.0,
        bank_insurance=1000.0,
        repayment_term=120,
        instalment_amount=100.0)

    return loan

