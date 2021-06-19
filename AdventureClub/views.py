from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse_lazy
from datetime import date
from django.views.generic import DetailView
from . import models
from .forms import clubRegisterationForm, SignUpForm, adventureEventform
from django.views.generic.edit import DeleteView, UpdateView, CreateView


# Create your views here.

def index(request):
    cities = models.AdventureClub.objects.values('city')
    clubs = ''
    featuredClubs = models.AdventureClub.objects.filter(featured=True)
    featuredEvents = models.AdventureEvent.objects.filter(featured=True)
    deleteEvent()
    if request.method == 'POST':
        query = request.POST.get('city')
        clubs = models.AdventureClub.objects.filter(city=query)
    sliderList = [1, 2, 3]
    context = {'user': request.user, 'city': cities, 'club': clubs, 'FC': featuredClubs, 'FE': featuredEvents,
               'sl': sliderList}
    return render(request, 'AdventureClubs/index.html', context)


def popedEvent(request, pk):
    poppedEvent = models.AdventureEvent.objects.filter(id=pk)
    context = {'pop': poppedEvent}
    return render(request, 'AdventureClubs/index.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        users_email = models.User.objects.all()
        if form.is_valid():
            for mail in users_email:
                if form.cleaned_data['email'] == mail.email:
                    # print("emails = ", mail.email)
                    messages.info(request, 'Use a different email, the email is already in use!')
                    return redirect('club:signUp')
            form.save()
            messages.info(request, "You are registered successfully!")
            return redirect('club:signIn')
    else:
        form = SignUpForm()
    context = {'form': form}
    return render(request, 'AdventureClubs/signUp.html', context)


def signIn(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user, backend=None)
                    messages.info(request, f"You are now logged in as {username}")
                    # return HttpResponseRedirect('/club/')
                    return redirect('club:index')
            else:
                form = AuthenticationForm()
                msg = "Incorrect username or password!"
                return render(request, 'AdventureClubs/SignIn.html', context={'msg': msg, 'form': form})
                # return redirect('club:signIn')
        else:
            form = AuthenticationForm()
            return render(request, 'AdventureClubs/SignIn.html', context={'form': form})
    else:
        return HttpResponseRedirect('/club/index/')


def signOut(request):
    logout(request)
    return redirect('club:signIn')


def RegisterClub(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = clubRegisterationForm(request.POST, request.FILES)
            if form.is_valid():
                form = form.save(commit=False)
                form.owner = request.user
                form.save()
                messages.success(request, 'Your adventure club is registered successfully!')
                return redirect('club:myClubs')
        form = clubRegisterationForm()
        return render(request, 'AdventureClubs/registerClub.html', context={'form': form, })
    else:
        return redirect('club:signIn')


def createEvent(request):
    if request.user.is_authenticated:
        clubs = models.AdventureClub.objects.filter(owner=request.user)
        if request.method == 'POST':
            form = adventureEventform(request.POST, request.FILES)
            print(form.errors)
            if form.is_valid():
                club = request.POST.get('club')
                # club_rec = models.AdventureClub.objects.filter(club_name=club).values(models.AdventureClub.pk)
                # club_rec = models.AdventureClub.objects.get(club_name=club)
                # print("Club Id", club_rec.pk)
                # form = form.save(commit=False)
                # form.event_by = club_rec.pk
                # form.save()
                # ev_by = club
                # club_ref = models.AdventureClub.objects.get(id=models.AdventureClub.objects.filter(club_name=club))
                # print(club_ref)
                # models.AdventureEvent.event_by = club_rec.pk
                title = form.cleaned_data['title']
                overview = form.cleaned_data['overview']
                image = form.cleaned_data['image']
                event_start_date = form.cleaned_data['event_start_date']
                event_end_date = form.cleaned_data['event_end_date']
                startpoint = form.cleaned_data['start_point']
                destinationpoint = form.cleaned_data['destination']
                eventmodelobj = models.AdventureEvent(event_by=models.AdventureClub.objects.get(club_name=club), title=title
                                                    , overview=overview, image=image
                                                    , event_start_date=event_start_date, event_end_date=event_end_date, start_point=startpoint, destination=destinationpoint)
                eventmodelobj.save()
                messages.success(request, 'Event is created successfully!')
                return redirect('club:events')
        form = adventureEventform()
        return render(request, 'AdventureClubs/adventureevent_form.html', context={'form': form, 'clubs': clubs, })
    else:
        return redirect('club:signIn')


def home(request):
    return render(request, 'AdventureClubs/home.html')


def myClubs(request):
    if request.user.is_authenticated:
        userClub = models.AdventureClub.objects.filter(owner=request.user)
        return render(request, "AdventureClubs/myClubs.html", context={'clubs': userClub})
    else:
        return redirect('club:signIn')


def onGoingEvents(request):
    events = models.AdventureEvent.objects.all()
    return render(request, "AdventureClubs/events.html", context={'event': events})


def searchResults(request):
    queryset = models.AdventureEvent.objects.all()
    query = request.GET.get('city')
    # print("--------------------------------------------", query)
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)

        ).distinct()

    context = {
        'FE': queryset
    }
    return render(request, 'AdventureClubs/search_results.html', context)


def clubDetail(request, pk):
    if request.user.is_authenticated:
        obj = models.AdventureClub.objects.filter(id=pk)
        obj1 = models.AdventureEvent.objects.filter(event_by=pk)
        context = {'fc': obj, 'fe': obj1}
        return render(request, 'AdventureClubs/clubDetail.html', context)
    else:
        return redirect('club:signIn')


class deleteClub(DeleteView):
    model = models.AdventureClub
    success_url = reverse_lazy('club:myClubs')
    template_name = 'AdventureClubs/adventureclub_confirm_delete.html'


class updateClub(UpdateView):
    model = models.AdventureClub
    fields = ('club_name', 'contact', 'email', 'club_image', 'club_address', 'city')
    success_url = reverse_lazy('club:myClubs')
    template_name = 'AdventureClubs/registerClub.html'


# def myEvents(request):
#     userEvents = models.AdventureEvent.objects.filter()
#     return render(request, "AdventureClubs/myEvents.html", context={'clubs': userEvents})

class eventDetails(DetailView):
    model = models.AdventureEvent
    context_object_name = 'fe'
    template_name = 'AdventureClubs/eventDetails.html'

def deleteEvent():
    expiredEvent = models.AdventureEvent.objects.all()

    for e in expiredEvent:
        if date.today() >= e.event_end_date:
            e.delete()