from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django.urls import reverse_lazy
from loan_helper.models import Client, Broker, Comment, Occupation, ClientOccupation, Bank, SuccessfulLoan
from loan_helper.forms import AddClientForm, UpdateClientForm


class IndexView(View):

    def get(self, request):
        return render(request, "index.html")


class ClientCreate(CreateView):
    model = Client
    success_url = '/all_clients/'
    form_class = AddClientForm


class BrokerCreate(CreateView):
    model = Broker
    fields = '__all__'
    success_url = '/all_brokers/'


class BankCreate(CreateView):
    model = Bank
    fields = '__all__'
    success_url = '/all_banks/'


class SuccessfulLoanCreate(CreateView):
    model = SuccessfulLoan
    fields = '__all__'
    success_url = '/all_successful_loans/'


class ClientListView(ListView):
    model = Client
    ordering = ['first_name']

    def get_context_data(self, **kwargs):
        context = super(ClientListView, self).get_context_data(**kwargs)
        context.update({
            'client_occupation': ClientOccupation.objects.all(),
        })
        return context

    def get_ordering(self):
        order = self.request.GET.get('order')
        if order:
            ordering = self.request.GET.get('ordering', order)
            return ordering


class BrokerListView(ListView):
    model = Broker
    ordering = ['name']


class BankListView(ListView):
    model = Bank
    ordering = ['name']


class SuccessfulLoanListView(ListView):
    model = SuccessfulLoan
    ordering = ['client']


class ClientDetailsView(View):

    def get(self, request, id):
        client = Client.objects.get(id=id)
        news = Comment.objects.filter(client_id=id)
        client_occupation = ClientOccupation.objects.filter(client=client)

        ctx = {
            'client': client,
            'news': news,
            'client_occupation': client_occupation
        }

        return render(request, 'client_details.html', ctx)

    def post(self, request, id):
        client = Client.objects.get(id=id)
        news = Comment.objects.filter(client_id=id)
        client_occupation = ClientOccupation.objects.filter(client=client)

        comment = request.POST.get('comment')
        submit = request.POST.get('submit')

        if comment and submit:
            Comment.objects.create(text=comment, client_id=id)

        ctx = {
            'client': client,
            'news': news,
            'client_occupation': client_occupation
        }

        return render(request, 'client_details.html', ctx)


class ClientUpdate(UpdateView):
    model = Client
    pk_url_kwarg = 'pk'
    form_class = UpdateClientForm

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        client_id = self.object.id
        self.object.save()
        return HttpResponseRedirect(f'/client_details/{client_id}')