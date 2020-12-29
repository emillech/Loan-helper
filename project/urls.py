"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from loan_helper.views import IndexView, ClientCreate, BrokerCreate, ClientDetailsView, ClientListView, ClientUpdate, \
    BankCreate, SuccessfulLoanCreate, BrokerListView, BankListView, SuccessfulLoanListView, ClientOccupationCreate, \
    BrokerDetailsView, BrokerUpdate, LoanUpdate, LoginView, LogoutView, GenerateDetailedReport, GenerateBrokerReport, \
    LoanCalculator

urlpatterns = [
    path('', IndexView.as_view()),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('add_client/', ClientCreate.as_view()),
    path('add_broker/', BrokerCreate.as_view()),
    path('add_bank/', BankCreate.as_view()),
    path('add_loan/', SuccessfulLoanCreate.as_view()),
    path('all_brokers/', BrokerListView.as_view()),
    path('all_banks/', BankListView.as_view()),
    path('all_loans/', SuccessfulLoanListView.as_view()),
    path('all_clients/', ClientListView.as_view()),
    path('client_details/<int:client_id>/', ClientDetailsView.as_view()),
    path('client_update/<int:pk>/', ClientUpdate.as_view()),
    path('income/<int:client_id>/', ClientOccupationCreate.as_view()),
    path('broker_details/<int:broker_id>/', BrokerDetailsView.as_view()),
    path('broker_update/<int:pk>/', BrokerUpdate.as_view()),
    path('loan_update/<int:pk>/', LoanUpdate.as_view()),
    path('detailed_report/', GenerateDetailedReport.as_view()),
    path('broker_report/', GenerateBrokerReport.as_view()),
    path('loan_calculator/', LoanCalculator.as_view()),
]
