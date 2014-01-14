from django.shortcuts import render
from django.template import RequestContext, loader
from employee_app.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.forms import ModelForm, BooleanField, MultipleChoiceField
from django.forms.models import modelform_factory, modelformset_factory
from django.db import transaction, IntegrityError
import datetime


def movies_view(request):
    movies_list = Movie.objects.all()
    context = {'movies_list':movies_list}
    return render(request, 'client/movies.html', context)


def projections_view(request, movie_id):
    projections_list = Projection.objects.filter(movie_id=movie_id, date_time__gt=datetime.datetime.now())
    context = {'projections_list':projections_list}
    return render(request, 'client/projections.html', context)


def seats_view(request, proj_id):
    error_message = ""

    if request.method == 'POST':
        form = ClientForm(request.POST)
        seats_nums = request.POST.getlist('seats_nums')
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    c = form.save()
                    for s in seats_nums:
                        r = Reservation()
                        r.client_id = c.id
                        r.projection_id = proj_id
                        r.seat_number = int(s)
                        r.save()

                    return HttpResponseRedirect('/client/')
            except IntegrityError:
                error_message = "Sorry, this seat is alreade not available, Someone was faster."

                
    else:
        form = ClientForm()

    reserved_seats = [r.seat_number for r in Reservation.objects.filter(projection_id=proj_id)]
    seats = Projection.objects.get(pk=proj_id).room.seats_number
    choices = [s for s in xrange(1, seats+1) if s not in reserved_seats]
    return render(request, 'client/seats.html', RequestContext(request, {'form':form, 'choices':choices, 'error_message':error_message}))




class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'surname', 'email', 'phone']