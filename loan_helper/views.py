from django.shortcuts import render
from django.views import View
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from loan_helper.models import Client, Broker, Comment, Occupation, ClientOccupation


class IndexView(View):

    def get(self, request):
        return render(request, "index.html")


class ClientCreate(CreateView):
    model = Client
    fields = '__all__'
    success_url = reverse_lazy('/all_clients/')


class BrokerCreate(CreateView):
    model = Broker
    fields = '__all__'
    success_url = reverse_lazy('')


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