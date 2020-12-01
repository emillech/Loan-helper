from faker import Faker
from loan_helper.models import Client, Broker, Occupation, ClientOccupation, Bank, SuccessfulLoan
import random

fake = Faker()


def add_client():
    for _ in range(100):
        all_brokers = Broker.objects.all()
        one_broker = random.choice(all_brokers)
        phone_number = random.randint(100000000, 999999999)
        current_status = random.randint(1, 7)
        occupation = random.randint(1, 4)
        monthly_income = random.randint(1000, 20000)
        marital_status = random.randint(1, 5)
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


def add_bank():
    Bank.objects.create(name='Alior Bank', address='Warsaw')
    Bank.objects.create(name='BNP Paribas', address='Warsaw')
    Bank.objects.create(name='Santander', address='Warsaw')
    Bank.objects.create(name='mBank', address='Warsaw')
    Bank.objects.create(name='Nest Bank', address='Warsaw')
    Bank.objects.create(name='Credit Agricole', address='Warsaw')
    Bank.objects.create(name='Skok', address='Warsaw')
    Bank.objects.create(name='Getin Bank', address='Warsaw')
    Bank.objects.create(name='Idea Bank', address='Warsaw')


def add_occupation():
    Occupation.objects.create(occupation=1)
    Occupation.objects.create(occupation=2)
    Occupation.objects.create(occupation=3)
    Occupation.objects.create(occupation=4)


def add_broker():
    for _ in range(30):
        Broker.objects.create(
            name=fake.company(),
            phone_number=random.randint(100000000, 999999999),
            email=fake.email()
        )


def add_successful_loan():
    # to nie jest dokladny sposob liczenia
    for _ in range(50):
        all_clients = Client.objects.all()
        client = random.choice(all_clients)
        broker = client.broker
        all_banks = Bank.objects.all()
        bank = random.choice(all_banks)
        loan_amount_net = random.randint(10000, 500000)
        bank_charge = random.randint(5, 15)
        interest_rate = random.randint(3, 10)
        bank_insurance = 0.05 * loan_amount_net
        repayment_term = random.randint(12, 120)
        loan_amount_gross = loan_amount_net + (loan_amount_net * (bank_charge / 100)) + bank_insurance
        instalment_amount = round(((loan_amount_gross * 0.3) / repayment_term), 2)
        SuccessfulLoan.objects.create(
            client=client,
            broker=broker,
            bank=bank,
            loan_amount_gross=loan_amount_gross,
            loan_amount_net=loan_amount_net,
            bank_charge=bank_charge,
            interest_rate=interest_rate,
            bank_insurance=bank_insurance,
            repayment_term=repayment_term,
            instalment_amount=instalment_amount,
        )


# add_bank()
# add_broker()
# add_occupation()
# add_client()
# add_successful_loan()