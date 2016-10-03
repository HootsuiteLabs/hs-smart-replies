import json
import requests

from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')

def get_articles(request):

    url = "https://aras.hootsuite.com/articles"
    querystring = {"q":"Advocacy,Social"}
    aras_response = requests.request("GET", url, params=querystring)

    # build the result
    response = {}
    response['result'] = aras_response
    response['message'] = ''
    return HttpResponse(json.dumps(response), content_type="application/json");


# def db(request):
#
#     greeting = Greeting()
#     greeting.save()
#
#     greetings = Greeting.objects.all()
#
#     return render(request, 'db.html', {'greetings': greetings})
