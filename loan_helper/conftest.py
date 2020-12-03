import pytest
from django.test import Client as Django_Client
from loan_helper.models import Client, Broker, Occupation, ClientOccupation
from faker import Faker
import random


fake = Faker()


@pytest.fixture
def django_client():
    django_client = Django_Client()
    return django_client


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
def client(new_broker: new_broker, new_occupation: new_occupation):
    one_broker = new_broker
    phone_number = random.randint(100000000, 999999999)
    current_status = random.randint(1, 7)
    one_client = Client.objects.create(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        phone_number=phone_number,
        email=fake.email(),
        address=fake.address(),
        broker=one_broker,
        current_status=current_status,
    )

    return one_client



