from django.db import models


MARITAL_STATUS = (
    (1, "Single"),
    (2, "Married with DoP"),
    (3, "Married without DoP"),
    (4, "Widow/Widower"),
)

CURRENT_STATUS = (
    (1, "Waiting for documents"),
    (2, "Sent to the bank"),
    (3, "Analysis in progress"),
    (4, "Negative decision"),
    (5, "Positive decision")
)

OCCUPATION = (
    (1, "Employment contract"),
    (2, "Mandate contract"),
    (3, "Small Business")
)


class Client(models.Model):
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16)
    phone_number = models.IntegerField()
    email = models.EmailField(null=True)
    marital_status = models.IntegerField(choices=MARITAL_STATUS)
    address = models.CharField(max_length=128, null=True)
    broker = models.ForeignKey('Broker', on_delete=models.CASCADE)
    current_status = models.IntegerField(choices=CURRENT_STATUS)
    date_created = models.DateField(auto_now_add=True, null=True)
    income = models.ManyToManyField('Occupation', through='ClientOccupation')


class Occupation(models.Model):
    occupation = models.IntegerField(choices=OCCUPATION)

    def __str__(self):
        return self.get_occupation_display()


class ClientOccupation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    occupation = models.ForeignKey(Occupation, on_delete=models.CASCADE)
    monthly_income = models.IntegerField(null=True)


class Broker(models.Model):
    name = models.CharField(max_length=128)
    phone_number = models.IntegerField()
    email = models.EmailField(null=True)

    def __str__(self):
        return self.name


class SuccessfulLoan(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    bank = models.ForeignKey('Bank', on_delete=models.CASCADE)
    loan_amount = models.IntegerField()


class Bank(models.Model):
    name = models.CharField(max_length=16)
    address = models.CharField(max_length=128)


class Comment(models.Model):
    text = models.TextField(null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)


