from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from datetime import datetime
from .models import Flight
from django.db.models import Q

def index(request):
    # if request.GET.get('search'):
    #     search = datetime.strptime(request.GET['search'], '%Y-%m-%d')
    #     flights = Flight.objects.filter(Q(startTime__day=search.day, startTime__month=search.month) |
    #                                     Q(endTime__day=search.day, endTime__month=search.month)).order_by('startTime')
    # else:
    #     flights = Flight.objects.all().order_by('startTime')
    #
    # template = loader.get_template('airport/mainpage.html')
    # context = {'flights_list' : flights}
    # return HttpResponse(template.render(context, request))
    return HttpResponse("You're looking the list of flights.")

