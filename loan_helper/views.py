from django.shortcuts import render
from django.views import View
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from loan_helper.models import Client, Broker


class IndexView(View):

    def get(self, request):
        return render(request, "index.html")


class ClientCreate(CreateView):
    model = Client
    fields = '__all__'
    exclude = ['news']
    success_url = reverse_lazy('')


class BrokerCreate(CreateView):
    model = Broker
    fields = '__all__'
    success_url = reverse_lazy('')