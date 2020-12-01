from faker import Faker
from loan_helper.models import Client, Broker, Occupation, ClientOccupation, Bank, SuccessfulLoan
import random

fake = Faker()


def add_client():
    for _ in range(10):
        all_brokers = Broker.objects.all()
        one_broker = random.choice(all_brokers)
        phone_number = random.randint(100000000, 999999999)
        current_status = random.randint(1, 7)
        occupation = random.randint(1, 5)
        monthly_income = random.randint(1000, 20000)
        marital_status = random.randint(1, 6)
        c1 = Client.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            phone_number=phone_number,
            email=fake.email(),
            address=fake.address(),
            broker=one_broker,
            current_status=current_status,
            marital_status=marital_status
        )
        o1 = Occupation.objects.get(id=occupation)
        ClientOccupation.objects.create(
            client=c1,
            occupation=o1,
            monthly_income=monthly_income
        )


def add_broker():
    for _ in range(10):
        Broker.objects.create(
            name=fake.company(),
            phone_number=random.randint(100000000, 999999999),
            email=fake.email()
        )

def add_successful_loan():
    all_clients = Client.objects.all()
    client = random.choice(all_clients)
    all_banks = Bank.objects.all()
    bank = random.choice(all_banks)
    loan_amount = random.randint(10000, 500000)
    SuccessfulLoan.objects.create(
        client=client,
        bank=bank,
        loan_amount=loan_amount
    )

add_successful_loan()