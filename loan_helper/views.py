from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, FormView
from django.urls import reverse_lazy
from loan_helper.models import Client, Broker, Comment, Occupation, ClientOccupation, Bank, SuccessfulLoan
from loan_helper.forms import AddClientForm, UpdateClientForm
from django.db.models import Q


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
    ordering = ['date_created']

    def get_context_data(self, **kwargs):
        context = super(ClientListView, self).get_context_data(**kwargs)
        context.update({
            'client_occupation': ClientOccupation.objects.all(),
        })
        return context

    def get_ordering(self):
        order = self.request.GET.get('order')
        sort = self.request.GET.get('sort')
        if sort:
            if order == "First Name":
                ordering = ['first_name']
                return ordering
            elif order == "Last Name":
                ordering = ['last_name']
                return ordering
            elif order == "Date Created":
                ordering = ['date_created']
                return ordering
            elif order == "Status":
                ordering = ['current_status']
                return ordering

    def get_queryset(self):
        search = self.request.GET.get('search')
        data_search = self.request.GET.get('data_search')
        object_list = self.model.objects.all()
        if search:
            object_list = object_list.filter(
                Q(first_name__icontains=data_search) |
                Q(last_name__icontains=data_search) |
                Q(phone_number__icontains=data_search) |
                Q(email__icontains=data_search) |
                Q(marital_status__icontains=data_search) |
                Q(address__icontains=data_search)
            )
        return object_list


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

        delete_comment = request.POST.get('delete_comment')
        comment = request.POST.get('comment')
        submit = request.POST.get('submit')

        if comment and submit:
            Comment.objects.create(text=comment, client_id=id)

        ctx = {
            'client': client,
            'news': news,
            'client_occupation': client_occupation
        }

        delete_client = request.POST.get('delete_client')
        if delete_client:
            client.delete()
            return redirect('/all_clients/')

        if delete_comment:
            pass

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


class ClientOccupationCreate(View):
    def get(self, request, client_id):
        client = Client.objects.get(id=client_id)
        client_occupation = ClientOccupation.objects.filter(client=client)

        ctx = {
            'client': client,
            'client_occupation': client_occupation
        }

        return render(request, 'income.html', ctx)

    def post(self, request, client_id):
        client = Client.objects.get(id=client_id)
        client_occupation = ClientOccupation.objects.filter(client=client)

        ctx = {
            'client': client,
            'client_occupation': client_occupation
        }

        add_occupation = request.POST.get('add_occupation')
        income = request.POST.get('income')
        remove = request.POST.get('remove')
        add = request.POST.get('add')
        remove_occupation = request.POST.get('remove_occupation')

        if add:
            chosen_job = ''
            if add_occupation == "1":
                chosen_job = Occupation(occupation=1)
                chosen_job.save()
            elif add_occupation == "2":
                chosen_job = Occupation(occupation=2)
                chosen_job.save()
            elif add_occupation == "3":
                chosen_job = Occupation(occupation=3)
                chosen_job.save()
            elif add_occupation == "4":
                chosen_job = Occupation(occupation=4)
                chosen_job.save()
            ClientOccupation.objects.create(client=client, occupation=chosen_job, monthly_income=income)

        # pomyslec co tu zrobic, gdy beda dwa takie same dochody, sytuacja raczej niemozliwa, ale kod sie wyjebie
        if remove:
            if remove_occupation == "Small Business":
                job = client.income.get(occupation=3)
                client_job = ClientOccupation.objects.filter(client=client, occupation=job)
                client_job.delete()
            elif remove_occupation == "Mandate contract":
                job = client.income.get(occupation=2)
                client_job = ClientOccupation.objects.filter(client=client, occupation=job)
                client_job.delete()
            elif remove_occupation == "Employment contract":
                job = client.income.get(occupation=1)
                client_job = ClientOccupation.objects.filter(client=client, occupation=job)
                client_job.delete()
            elif remove_occupation == "Pension":
                job = client.income.get(occupation=4)
                client_job = ClientOccupation.objects.filter(client=client, occupation=job)
                client_job.delete()

        return render(request, 'income.html', ctx)