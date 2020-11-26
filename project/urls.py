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
from loan_helper.views import IndexView, ClientCreate, BrokerCreate, ClientDetailsView, ClientListView, ClientUpdate

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view()),
    path('add_client/', ClientCreate.as_view()),
    path('add_broker/', BrokerCreate.as_view()),
    path('client_details/<int:id>/', ClientDetailsView.as_view()),
    path('all_clients/', ClientListView.as_view()),
    path('client_update/<int:pk>/', ClientUpdate.as_view()),
]
