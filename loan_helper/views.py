from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, FormView
from loan_helper.models import Client, Broker, Comment, Occupation, ClientOccupation, Bank, SuccessfulLoan, \
    CURRENT_STATUS, OCCUPATION
from loan_helper.forms import AddClientForm, UpdateClientForm, LoginForm, LoanCalculatorForm
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from loan_helper.utils import render_to_pdf
from datetime import date
import numpy as np


class LoginView(FormView):
    """
    A class used to represent a Login View. It uses custom form.
    """

    form_class = LoginForm
    template_name = "login.html"
    success_url = "/"

    def form_valid(self, form):
        """
        This method checks if user is authenticated, if is, it allows to log in.
        If not, user will see error text.
        """

        username = form.cleaned_data["login"]
        password = form.cleaned_data["password"]
        user = authenticate(self.request, username=username, password=password)
        if user:
            login(self.request, user)
            return super().form_valid(form)
        form.add_error(None, "Invalid login or password")
        return super().form_invalid(form)


class LogoutView(View):
    """
    A class used to represent a Logout. It does not need template.
    """

    def get(self, request):
        """
        This method logout user and redirect him to index.
        """
        logout(request)
        return redirect("/")


class IndexView(View):
    """
    A class used to represent a Index View.
    """

    def get(self, request):
        """
        This method render index template and checks if user is authenticated. User is passes in context.
        """

        user = request.user
        if user.is_authenticated:
            user = User.objects.get(username='root')
        else:
            user = 'Anonymous'

        return render(request, "index.html", {'user': user})


class ClientCreate(LoginRequiredMixin, CreateView):
    """
    A class used to represent a Client Create View. It allows to add client to database through custom form.
    """

    model = Client
    success_url = '/all_clients/'
    form_class = AddClientForm
    login_url = '/login/'


class BrokerCreate(LoginRequiredMixin, CreateView):
    """
    A class used to represent a Broker Create View. It allows to add broker to database through template form.
    """

    model = Broker
    fields = '__all__'
    success_url = '/all_brokers/'
    login_url = '/login/'


class BankCreate(LoginRequiredMixin, CreateView):
    """
    A class used to represent a Bank Create View. It allows to add bank to database through template form.
    """

    model = Bank
    fields = '__all__'
    success_url = '/all_banks/'
    login_url = '/login/'


class SuccessfulLoanCreate(LoginRequiredMixin, CreateView):
    """
    A class used to represent a Successful Loan Create View.
    It allows to add successful loan to database through template form.
    """

    model = SuccessfulLoan
    fields = '__all__'
    success_url = '/all_loans/'
    login_url = '/login/'


class ClientListView(LoginRequiredMixin, ListView):
    """
    A class used to represent a Client List View. It shows all client from database with specific pagination.
    Clients are ordered by date created.
    """

    model = Client
    ordering = 'date_created'
    paginate_by = 15
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        """
        This method return specific context. At this point only ClientOccupation objects are passed.
        """

        context = super(ClientListView, self).get_context_data(**kwargs)
        context.update({
            'client_occupation': ClientOccupation.objects.all(),
        })
        return context

    def get_ordering(self):
        """
        This method allows to use sorting. It overwrite default ordering.
        """

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
                ordering = '-date_created'
                return ordering
            elif order == "Status":
                ordering = 'current_status'
                return ordering

    def get_queryset(self):
        """
        This method allows to use search engine. Search engine looks for specific words in main fields.
        """

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
    """
    A class used to represent a Broker List View. It shows all brokers from database with specific pagination.
    Brokers are ordered by name.
    """

    model = Broker
    ordering = ['name']
    paginate_by = 15
    login_url = '/login/'


class BankListView(LoginRequiredMixin, ListView):
    """
    A class used to represent a Bank List View. It shows all banks from database.
    Banks are ordered by name.
    """

    model = Bank
    ordering = ['name']
    login_url = '/login/'


class SuccessfulLoanListView(LoginRequiredMixin, ListView):
    """
    A class used to represent a Successful Loan List View. It shows all loans from database with specific pagination.
    Loans are ordered by date created descending.
    """

    model = SuccessfulLoan
    ordering = '-date_created'
    paginate_by = 15
    login_url = '/login/'

    def get_ordering(self):
        """
        This method allows to use sorting. It overwrite default ordering.
        """

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
    """
    A class used to represent a Client Details View. It shows all information about chosen client.
    """

    login_url = '/login/'

    def get(self, request, client_id):
        """
        This method allows to pass context. It renders proper template.
        """

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
        """
        This method allows to manage comments section and delete client. It passes context and renders proper template.
        """

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
    """
    A class used to represent a Broker Details View. It shows all information about chosen broker.
    """

    login_url = '/login/'

    def get(self, request, broker_id):
        """
        This method allows to pass context. It renders proper template.
        """

        broker = Broker.objects.get(id=broker_id)
        all_clients = Client.objects.filter(broker=broker)
        all_loans = SuccessfulLoan.objects.filter(broker=broker)

        ctx = {
            'broker': broker,
            'clients': all_clients,
            'loans': all_loans
        }

        return render(request, 'broker_details.html', ctx)


class ClientUpdate(LoginRequiredMixin, UpdateView):
    """
    A class used to represent a Client Update View. It allows to change the same field as Create View.
    """

    model = Client
    pk_url_kwarg = 'pk'
    form_class = UpdateClientForm
    login_url = '/login/'

    def form_valid(self, form):
        """
        If the form is valid, update db and redirect to the supplied URL.
        """

        client_id = self.object.id
        self.object.save()
        return HttpResponseRedirect(f'/client_details/{client_id}')


class BrokerUpdate(LoginRequiredMixin, UpdateView):
    """
    A class used to represent a Broker Update View. It allows to change the same field as Broker View.
    """

    model = Broker
    pk_url_kwarg = 'pk'
    fields = '__all__'
    login_url = '/login/'

    def form_valid(self, form):
        """
        If the form is valid, update db and redirect to the supplied URL.
        """

        broker_id = self.object.id
        self.object.save()
        return HttpResponseRedirect(f'/client_details/{broker_id}')


class LoanUpdate(LoginRequiredMixin, UpdateView):
    """
    A class used to represent a Broker Update View. It allows to change the same field as Broker View.
    """

    model = SuccessfulLoan
    pk_url_kwarg = 'pk'
    fields = '__all__'
    success_url = '/all_loans/'
    login_url = '/login/'


class ClientOccupationCreate(LoginRequiredMixin, View):
    """
    A class used to represent a ClientOccupation Create View.
    It allows to add or remove specific occupation and income to client and save it to db. It uses custom form.
    """

    login_url = '/login/'

    def get(self, request, client_id):
        """
        This method allows to pass context. It renders proper template.
        """

        client = Client.objects.get(id=client_id)
        client_occupation = ClientOccupation.objects.filter(client=client)

        ctx = {
            'client': client,
            'client_occupation': client_occupation,
            'occupation': OCCUPATION
        }

        return render(request, 'income.html', ctx)

    def post(self, request, client_id):
        """
        This method allows to manage client's occupation. It passes context and renders proper template.
        """

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

        # TODO: naprawić błąd, kod sie wykrzacza jak chcemy usunąć dwa takie same dochody
        if remove:
            for key, item in dict(OCCUPATION).items():
                if remove_occupation == item:
                    job = client.income.get(occupation=key)
                    client_job = ClientOccupation.objects.filter(client=client, occupation=job)
                    client_job.delete()

        return render(request, 'income.html', ctx)


class GenerateDetailedReport(View):
    def get(self, request, *args, **kwargs):
        clients = Client.objects.all()

        ctx = {
            'clients': clients
        }

        return render(request, 'pdf/daily_report_data.html', ctx)

    def post(self, request):
        chosen_clients = request.POST.getlist('choice')
        clients = []
        client_data = {

        }
        today = date.today()
        for client in chosen_clients:
            client = Client.objects.get(id=client)
            comments = Comment.objects.filter(client=client)
            client_comments = []
            client_data.update({f'{client} - {client.get_current_status_display()}': client_comments})
            for comment in comments:
                client_comments.append(f'{comment.text} - {comment.date_created.strftime("%b %d %Y %H:%M:%S")}')

        ctx = {
            'data': client_data,
            'clients': clients,
            'date': today
        }

        # pdf has issue with polish letters
        # return render(request, 'pdf/daily_report.html', ctx)
        pdf = render_to_pdf('pdf/daily_report.html', ctx)
        return pdf


class GenerateBrokerReport(View):
    def get(self, request, *args, **kwargs):
        brokers = Broker.objects.all()

        ctx = {
            'brokers': brokers
        }

        return render(request, 'pdf/broker_report_data.html', ctx)

    def post(self, request):
        chosen_brokers = request.POST.getlist('choice')
        today = date.today()
        brokers_data = {

        }

        for broker in chosen_brokers:
            broker = Broker.objects.get(id=broker)
            clients = Client.objects.filter(broker=broker)
            client_data = []
            for client in clients:
                loans = SuccessfulLoan.objects.filter(client=client)
                loans_data = []
                for loan in loans:
                    loans_data.append(f'{loan.bank} - {loan.loan_amount_gross}')
                if loans_data:
                    client_data.append(f'{client} - {client.get_current_status_display()} - {loans_data} gross')
                client_data.append(f'{client} - {client.get_current_status_display()}')
            brokers_data.update({broker: client_data})

        ctx = {
            'date': today,
            'data': brokers_data
        }

        # pdf has issue with polish letters
        return render(request, 'pdf/daily_report.html', ctx)
        # pdf = render_to_pdf('pdf/broker_report.html', ctx)
        # return pdf


class LoanCalculator(View):

    def get(self, request):
        form = LoanCalculatorForm
        ctx = {
            'form': form
        }
        return render(request, 'loan_calculator.html', ctx)

    def post(self, request):
        net_amount = int(request.POST.get("net_amount"))
        bank_charge = float(request.POST.get("bank_charge"))
        interest_rate = float(request.POST.get("interest_rate"))
        repayment_term = int(request.POST.get("repayment_term"))
        insurance = float(request.POST.get("insurance"))

        gross_amount = net_amount + (bank_charge / 100) * net_amount + insurance

        instalment = round(abs(np.pmt((interest_rate / 100) / 12, repayment_term, gross_amount)), 2)

        ctx = {
            'instalment': instalment
        }

        return render(request, 'loan_calculator.html', ctx)

