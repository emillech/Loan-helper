from django.db import models


MARITAL_STATUS = (
    (1, "Single"),
    (2, "Married with DoP"),
    (3, "Married without DoP"),
    (4, "Widow/Widower"),
    (5, "Divorced")
)

CURRENT_STATUS = (
    (1, 'New Client'),
    (2, "Waiting for documents"),
    (3, "Sent to the bank"),
    (4, 'Offer'),
    (5, "Analysis in progress"),
    (6, "Negative decision"),
    (7, "Positive decision"),
    (8, "Client resign")
)

OCCUPATION = (
    (1, "Employment contract"),
    (2, "Mandate contract"),
    (3, "Small Business"),
    (4, "Pension")
)


class Client(models.Model):
    """
    A class used to represent a Client. Most of fields define personal data information.
    """
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16)
    phone_number = models.IntegerField()
    email = models.EmailField(null=True)
    marital_status = models.IntegerField(choices=MARITAL_STATUS, null=True)
    address = models.CharField(max_length=128, null=True)
    broker = models.ForeignKey('Broker', on_delete=models.CASCADE)
    current_status = models.IntegerField(choices=CURRENT_STATUS)
    date_created = models.DateField(auto_now_add=True, null=True)
    income = models.ManyToManyField('Occupation', through='ClientOccupation')

    def __str__(self):
        """
        This method allow to represent model Client with only first name and last name.
        """
        return f'{self.first_name} {self.last_name}'


class Occupation(models.Model):
    """
    A class used to represent an Occupation. It uses choices from tuple of tuples - OCCUPATION.
    """
    occupation = models.IntegerField(choices=OCCUPATION)

    def __str__(self):
        """
        This method allow to represent model Occupation with str from tuple.
        """
        return self.get_occupation_display()


class ClientOccupation(models.Model):
    """
    A class used to represent a Client Occupation. This is through table.
    It is related to client model and occupation model.
    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    occupation = models.ForeignKey(Occupation, on_delete=models.CASCADE)
    monthly_income = models.IntegerField(null=True)


class Broker(models.Model):
    """
    A class used to represent a Broker.
    """
    name = models.CharField(max_length=128)
    phone_number = models.IntegerField()
    email = models.EmailField(null=True)

    def __str__(self):
        """
        This method allow to represent model Broker with only name.
        """
        return self.name


class SuccessfulLoan(models.Model):
    """
    A class used to represent a successful loan. Every field define specific information about banking loan.
    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE)
    bank = models.ForeignKey('Bank', on_delete=models.CASCADE)
    loan_amount_gross = models.IntegerField()
    loan_amount_net = models.FloatField()
    bank_charge = models.FloatField()
    interest_rate = models.FloatField()
    bank_insurance = models.FloatField(null=True)
    repayment_term = models.IntegerField()
    instalment_amount = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)


class Bank(models.Model):
    """
    A class used to represent a successful Bank.
    """
    name = models.CharField(max_length=16)
    address = models.CharField(max_length=128)

    def __str__(self):
        """
        This method allow to represent model Broker with only name.
        """
        return self.name


class Comment(models.Model):
    """
    A class used to represent a Comment. Comments are related to specific clients.
    """
    text = models.TextField(null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)


