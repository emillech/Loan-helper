from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, FormView
from django.urls import reverse_lazy
from loan_helper.models import Client, Broker, Comment, Occupation, ClientOccupation, Bank, SuccessfulLoan, \
    CURRENT_STATUS, OCCUPATION
from loan_helper.forms import AddClientForm, UpdateClientForm, LoginForm
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginView(FormView):
    form_class = LoginForm
    template_name = "login.html"
    success_url = "/"

    def form_valid(self, form):
        username = form.cleaned_data["login"]
        password = form.cleaned_data["password"]
        user = authenticate(self.request, username=username, password=password)
        if user:
            login(self.request, user)
            return super().form_valid(form)
        # Wykona nie na formularzu add_error(None, String) powoduje, że zostanie dodany błąd
        # nie związany z żadnym polem formularza, przydatne w przypadku, błąd jest związany
        # wieloma polami. Podanie add_error z pierwszym parametrem stringowym powoduje, że dany
        # błąd zostanie dodany do kola o takiej nazwie.
        form.add_error(None, "Zły login lub hasło")
        return super().form_invalid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("/")


class IndexView(View):

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            user = User.objects.get(username='root')
        else:
            user = 'Anonymous'

        return render(request, "index.html", {'user': user})


class ClientCreate(LoginRequiredMixin, CreateView):
    model = Client
    success_url = '/all_clients/'
    form_class = AddClientForm
    login_url = '/login/'


class BrokerCreate(LoginRequiredMixin, CreateView):
    model = Broker
    fields = '__all__'
    success_url = '/all_brokers/'
    login_url = '/login/'


class BankCreate(LoginRequiredMixin, CreateView):
    model = Bank
    fields = '__all__'
    success_url = '/all_banks/'
    login_url = '/login/'


class SuccessfulLoanCreate(LoginRequiredMixin, CreateView):
    model = SuccessfulLoan
    fields = '__all__'
    success_url = '/all_loans/'
    login_url = '/login/'


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    ordering = 'date_created'
    paginate_by = 15
    login_url = '/login/'

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
                ordering = 'first_name'
                return ordering
            elif order == "Last Name":
                ordering = 'last_name'
                return ordering
            elif order == "Date Created":
                ordering = 'date_created'
                return ordering
            elif order == "Status":
                ordering = 'current_status'
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
        ordering = self.get_ordering()

        if ordering and isinstance(ordering, str):
            object_list = object_list.order_by(ordering)
        return object_list


class BrokerListView(LoginRequiredMixin, ListView):
    model = Broker
    ordering = ['name']
    paginate_by = 15
    login_url = '/login/'


class BankListView(LoginRequiredMixin, ListView):
    model = Bank
    ordering = ['name']
    login_url = '/login/'


class SuccessfulLoanListView(LoginRequiredMixin, ListView):
    model = SuccessfulLoan
    ordering = ['-date_created']
    paginate_by = 15
    login_url = '/login/'

    def get_ordering(self):
        order = self.request.GET.get('order')
        sort = self.request.GET.get('sort')
        if sort:
            if order == "Client":
                ordering = 'client'
                return ordering
            elif order == "Bank":
                ordering = 'bank'
                return ordering
            elif order == "Newest":
                ordering = '-date_created'
                return ordering
            elif order == "Oldest":
                ordering = 'date_created'
                return ordering


class ClientDetailsView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, client_id):
        client = Client.objects.get(id=client_id)
        news = Comment.objects.filter(client_id=client_id)
        client_occupation = ClientOccupation.objects.filter(client=client)
        client_loans = SuccessfulLoan.objects.filter(client=client)
        ctx = {
            'client': client,
            'news': news,
            'client_occupation': client_occupation,
            'client_loans': client_loans,
            'all_status': CURRENT_STATUS
        }

        return render(request, 'client_details.html', ctx)

    def post(self, request, client_id):
        client = Client.objects.get(id=client_id)
        news = Comment.objects.filter(client_id=client_id)
        client_occupation = ClientOccupation.objects.filter(client=client)
        client_loans = SuccessfulLoan.objects.filter(client=client)

        delete_comment = request.POST.get('delete_comment')
        comment = request.POST.get('comment')
        add_new_comment = request.POST.get('add_new_comment')
        change_status = request.POST.get('change_status')
        new_status = request.POST.get('new_status')
        delete_client = request.POST.get('delete_client')
        comment_id = request.POST.get('comment_id')

        if comment and add_new_comment:
            Comment.objects.create(text=comment, client_id=client_id)

        ctx = {
            'client': client,
            'news': news,
            'client_occupation': client_occupation,
            'all_status': CURRENT_STATUS,
            'client_loans': client_loans,
        }

        if change_status:
            dictionary = dict(CURRENT_STATUS)
            for key, item in dictionary.items():
                if new_status == item:
                    client.current_status = key
                    client.save()
                    return render(request, 'client_details.html', ctx)

        if delete_client:
            client.delete()
            return redirect('/all_clients/')

        if delete_comment:
            comment_to_delete = Comment(id=comment_id)
            comment_to_delete.delete()
            return render(request, 'client_details.html', ctx)

        return render(request, 'client_details.html', ctx)


class BrokerDetailsView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, broker_id):
        broker = Broker.objects.get(id=broker_id)
        all_clients = Client.objects.filter(broker=broker)
        all_loans = SuccessfulLoan.objects.filter(broker=broker)

        ctx = {
            'broker': broker,
            'clients': all_clients,
            'loans': all_loans
        }

        return render(request, 'broker_details.html', ctx)

    def post(self, request, broker_id):
        return render(request, 'broker_details.html')


class ClientUpdate(LoginRequiredMixin, UpdateView):
    model = Client
    pk_url_kwarg = 'pk'
    form_class = UpdateClientForm
    login_url = '/login/'

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        client_id = self.object.id
        self.object.save()
        return HttpResponseRedirect(f'/client_details/{client_id}')


class BrokerUpdate(LoginRequiredMixin, UpdateView):
    model = Broker
    pk_url_kwarg = 'pk'
    fields = '__all__'
    login_url = '/login/'

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        broker_id = self.object.id
        self.object.save()
        return HttpResponseRedirect(f'/client_details/{broker_id}')


class LoanUpdate(LoginRequiredMixin, UpdateView):
    model = SuccessfulLoan
    pk_url_kwarg = 'pk'
    fields = '__all__'
    success_url = '/all_loans/'
    login_url = '/login/'


class ClientOccupationCreate(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, client_id):
        client = Client.objects.get(id=client_id)
        client_occupation = ClientOccupation.objects.filter(client=client)

        ctx = {
            'client': client,
            'client_occupation': client_occupation,
            'occupation': OCCUPATION
        }

        return render(request, 'income.html', ctx)

    def post(self, request, client_id):
        client = Client.objects.get(id=client_id)
        client_occupation = ClientOccupation.objects.filter(client=client)

        ctx = {
            'client': client,
            'client_occupation': client_occupation,
            'occupation': OCCUPATION
        }

        add_occupation = request.POST.get('add_occupation')
        income = request.POST.get('income')
        remove = request.POST.get('remove')
        add = request.POST.get('add')
        remove_occupation = request.POST.get('remove_occupation')

        if add:
            int(add_occupation)
            chosen_job = Occupation(occupation=add_occupation)
            chosen_job.save()
            ClientOccupation.objects.create(client=client, occupation=chosen_job, monthly_income=income)

        # pomyslec co tu zrobic, gdy beda dwa takie same dochody, sytuacja raczej niemozliwa, ale kod sie wyjebie
        if remove:
            for key, item in dict(OCCUPATION).items():
                if remove_occupation == item:
                    job = client.income.get(occupation=key)
                    client_job = ClientOccupation.objects.filter(client=client, occupation=job)
                    client_job.delete()

        return render(request, 'income.html', ctx)