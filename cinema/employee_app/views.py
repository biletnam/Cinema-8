from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader
from employee_app.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.forms import ModelForm, BooleanField
from django.forms.models import modelform_factory, modelformset_factory
from django.db import transaction
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError


def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/employee/index/')
                else:
                    return HttpResponse('Your account is disabled')
            else:
                return HttpResponse('username or login incorrect')
    else:
        form = LoginForm()
    return render(request, 'employee_app/login.html', RequestContext(request, {'form':LoginForm}))

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/employee/')



@login_required(redirect_field_name='/employee/login/')
def index(request):
    pages = {
        'Manage movies':'movies',
        'Manage rooms':'rooms',
        'Reservations':'reservations',
        }
    context = {'pages':pages}
    return render(request, 'employee_app/index.html', context)


@login_required(redirect_field_name='/employee/login/')
def movies(request):
    movies_list = Movie.objects.all()
    context = {'movies_list':movies_list}
    return render(request, 'employee_app/movies.html', context)


@login_required(redirect_field_name='/employee/login/')
def edit_movie(request, movie_id):
    ProjectionsFormSet = modelformset_factory(Projection, form=ProjectionForm, extra=6, can_delete=True)
    movie = Movie.objects.get(pk=movie_id)
    if request.method == 'POST':
        movieForm = MovieFormEdit(request.POST)
        projectionsForms = ProjectionsFormSet(request.POST)
        
        if movieForm.is_valid() and projectionsForms.is_valid():
            
            if( movieForm.cleaned_data['delete'] ):
                with transaction.atomic():
                    movie.delete()
            else:    
                with transaction.atomic():
                    projections = projectionsForms.save(commit=False)
                    for p in projections:
                        p.movie_id = movie.id
                        p.save()

            return HttpResponseRedirect('/employee/movies/')
    else:
        movieForm = MovieFormEdit(instance = Movie.objects.get(pk=movie_id))
        projectionsForms = ProjectionsFormSet(queryset=Projection.objects.filter(movie_id=movie_id))

    for k,v in movieForm.fields.iteritems():
        v.widget.attrs['readonly'] = True
    
    return render(request, 'employee_app/edit_movie.html', RequestContext(request, {'movieForm':movieForm, 'id':movie_id, 'projectionsForms':projectionsForms, 'movie':movie}))


@login_required(redirect_field_name='/employee/login/')
def add_movie(request):
    ProjectionsFormSet = modelformset_factory(Projection, form=ProjectionForm, extra=6)
    if request.method == 'POST':
        
        movieForm = MovieFormAdd(request.POST)
        projectionsForms = ProjectionsFormSet(request.POST)
        
        if movieForm.is_valid() and projectionsForms.is_valid():
            
            with transaction.atomic():
                movie = movieForm.save(commit=False) 
                projections = projectionsForms.save(commit=False)
                movie.save()
                for p in projections:
                    p.movie_id = movie.id
                    p.save()

            return HttpResponseRedirect('/employee/movies/')
    else:
        movieForm = MovieFormAdd()
        projectionsForms = ProjectionsFormSet(queryset=Projection.objects.none())

    return render(request, 'employee_app/edit_movie.html', RequestContext(request, {'movieForm':movieForm, 'projectionsForms':projectionsForms}))



@login_required(redirect_field_name='/employee/login/')
def rooms(request):
    rooms_list = Room.objects.all()
    context = {'rooms_list':rooms_list}
    return render(request, 'employee_app/rooms.html', context)


@login_required(redirect_field_name='/employee/login/')
def edit_room(request, room_id):
    if request.method == 'POST':
        roomForm = RoomFormEdit(request.POST)

        if roomForm.is_valid():
            room = Room()
            room.room_number = room_id
            room.seats_number = roomForm.cleaned_data['seats_number']
            room.status = roomForm.cleaned_data['status']
        
            if( roomForm.cleaned_data['delete'] ):
                with transaction.atomic():
                    room = Room.objects.get(pk=room.room_number)
                    room.delete()
            else:
                room.save()

            return HttpResponseRedirect('/employee/rooms/')
    else:
        roomForm = RoomFormEdit(instance = Room.objects.get(pk=room_id))

    return render(request, 'employee_app/edit_room.html', RequestContext(request, {'roomForm':roomForm, 'id':room_id}))


@login_required(redirect_field_name='/employee/login/')
def add_room(request):
    if request.method == 'POST':
        roomForm = RoomFormAdd(request.POST)

        if roomForm.is_valid():
            room = Room()
            room.room_number = roomForm.cleaned_data['room_number']
            room.seats_number = roomForm.cleaned_data['seats_number']
            room.status = roomForm.cleaned_data['status']
            room.save()

            return HttpResponseRedirect('/employee/rooms/')
    else:
        roomForm = RoomFormAdd()

    return render(request, 'employee_app/edit_room.html', RequestContext(request, {'roomForm':roomForm}))



@login_required(redirect_field_name='/employee/login/')
def reservations(request): 
    if request.method == 'POST':
        searchForm = SearchForm(request.POST)

        if searchForm.is_valid():
            try:
                resId = int(searchForm.cleaned_data['search'])
                try:
                    r = Reservation.objects.get(pk=resId)
                    return HttpResponseRedirect(reverse('view_reservation', kwargs={'id':str(resId)}))
                except Reservation.DoesNotExist:
                    reservations_list = Reservation.objects.all()
            except ValueError:
                text=searchForm.cleaned_data['search']
                reservations_list = Reservation.objects.filter(Q(client__name__contains=text) | Q(client__surname__contains=text)) 
    else:
        reservations_list = Reservation.objects.all()
        searchForm = SearchForm()

    context = {'reservations_list':reservations_list, 'searchForm':searchForm}
    return render(request, 'employee_app/reservations.html', RequestContext(request, context))


@login_required(redirect_field_name='/employee/login/')
def view_reservation(request, id):
    res = Reservation.objects.get(pk=id)
    if request.method == 'POST':
        reservationForm = ReservationForm(request.POST)

        if reservationForm.is_valid():
            if reservationForm.cleaned_data['received']:
                res.received = True
            else:
                res.received = False
            
            res.save()
            return HttpResponseRedirect('/employee/reservations/')
    else:
        reservationForm = ReservationForm(instance=res)


    return render(request, 'employee_app/view_reservation.html', RequestContext(request, {'reservationForm':reservationForm, 'reservation':res}))



#Forms###########
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class SearchForm(forms.Form):
    search = forms.CharField(required=False)


class MovieFormEdit(ModelForm):
    delete = BooleanField(required=False)
    class Meta:
        model = Movie
        fields = ['length', 'minimal_age', 'genre']



class MovieFormAdd(ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'length', 'minimal_age', 'genre']


class ProjectionForm(ModelForm):
    class Meta:
        model = Projection
        fields = ['room', 'date_time', 'ticket_price', 'audio_language', 'subtitles_language']

    def __init__(self, *args, **kwargs):
        super(ProjectionForm,self).__init__(*args, **kwargs)
        self.fields['room'].queryset = Room.objects.filter(status='Open')

class RoomFormAdd(ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'seats_number', 'status']

class RoomFormEdit(ModelForm):
    delete = BooleanField(required=False)
    class Meta:
        model = Room
        fields = ['seats_number', 'status']

class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ['received']


