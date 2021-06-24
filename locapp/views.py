from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from .models import Destination, Tourist, DestinationCityDetails, DestinationMetaDetails, PlaceRatings
from locapp.forms import DestinationForm, TouristForm, UserCityForm, UserPlaceForm, PlaceRatingForm
from django.contrib.auth import logout
from .utils import location_module
from django.contrib import messages
from geopy.geocoders import Nominatim

# Create your views here.
def soclogin(request):
    return render(request, 'locapp/login.html')

def DestinationView(request):
    u_ip = request.META["REMOTE_ADDR"]
    map=''
    uname = request.user.username
    if request.method == "POST":
        fm = DestinationForm(request.POST)
        if fm.is_valid():
            fmwait = fm.save(commit=False)
            destination_ = request.POST.get('destination')
            loc_details=DestinationCityDetails.objects.filter(destination_name__icontains=destination_)
            if not loc_details.exists():
                messages.info(request, "The Location that you are Searching for has not yet been included :(")
                return redirect(reverse('locapp:dest'))
            dest_details=location_module(loc_details[0],u_ip)
            print(dest_details)

            distance=dest_details.pop(0)
            map = dest_details.pop(0)
            dest_meta_details = dest_details.pop(0)
            tourist_lat = dest_details.pop(0)
            tourist_lon = dest_details.pop(0)
            tourist_locdetails = dest_details.pop(0)
            dest_lat=dest_details.pop(0)
            dest_lon=dest_details.pop(0)
            fmwait.destination = destination_
            fmwait.distance=distance

            fmwait.save()
            touristobj = Tourist(tourist_name=uname,
            tourist_latitude= tourist_lat, tourist_longitude=tourist_lon, tourist_location = tourist_locdetails)
            touristobj.save()

            fm = DestinationForm()
            return render(request,'locapp/locationdetails.html', context={'form':fm, 'map': map,
                    'username':uname,'dest_details': loc_details, 'distance': distance, 'dest_meta_details':dest_meta_details,
                                              'tourist_lat':tourist_lat,'tourist_lon':tourist_lon,'dest_lat':dest_lat,'dest_lon':dest_lon})

    

    popular_dest=DestinationMetaDetails.objects.filter(admin_approved=True,place_rating__in=[4,5])
    fm = DestinationForm()
    obj = DestinationCityDetails.objects.filter(admin_approved=True, city_rating__in=[4,5])[0:8]
    obj1 = DestinationCityDetails.objects.filter(admin_approved=True).order_by('?')[0:8]
    all_obj=DestinationCityDetails.objects.filter(admin_approved=True)

    sl=[1,2,3]
        
    return render(request,'locapp/index.html',
                  context={'form':fm, 'map': map,'username':uname,'sl':sl,'obj':obj,'popular':popular_dest,'obj1':obj1,'allObj':all_obj})



def dest_view2(request,pk):
    u_ip = request.META["REMOTE_ADDR"]
    obj=DestinationCityDetails.objects.filter(id=pk)
    details=location_module(obj[0],u_ip)
    distance=details[0]
    mapobj=details[1]
    dest_meta_details=details[2]
    tourist_lat = details[3]
    tourist_lon = details[4]
    context={'dest_details':obj,'distance':distance,'map':mapobj,'dest_meta_details':dest_meta_details
             ,'tourist_lat':tourist_lat,'tourist_lon':tourist_lon,'dest_lat':details[6],'dest_lon':details[7]}
    return render(request,'locapp/locationdetails.html',context)


def logoutuser(request):
    logout(request)
    return redirect('/')


def loc_meta_view(request, pk):
    dest_meta_details = DestinationMetaDetails.objects.filter(id = pk)
    dest_details=location_module(dest_meta_details[0])

    if dest_details == 'not found':
        return render(request, 'locapp/meta_dest_error_details.html', context={'dest_meta_details':dest_meta_details})
    else:
        distance = dest_details.pop(0)
        map = dest_details.pop(0)
        dest_meta = dest_details.pop(0)
        tourist_lat = dest_details.pop(0)
        tourist_lon = dest_details.pop(0)
        tourist_locdetails = dest_details.pop(0)
        dest_lat = dest_details.pop(0)
        dest_lon = dest_details.pop(0)
        return render(request, 'locapp/meta_dest_map.html',
            context={'dest_meta_details': dest_meta_details,'map':map,'distance':distance,
                    'tourist_lat':tourist_lat,'tourist_lon':tourist_lon,'dest_lat':dest_lat,'dest_lon':dest_lon})



def usercityform(request):
    if request.user.is_authenticated:
        rating_count = 0
        rating_sum = 0
        citydetails = DestinationCityDetails.objects.all()
        if request.method == 'POST':
            form = UserCityForm(request.POST, request.FILES)
            cityname = request.POST.get('destination_name')
            cityname = cityname.upper()
            rating = request.POST.get('rating')
            placeratinginfo = PlaceRatings.objects.filter(user_info=request.user, place_name=cityname)
            if not placeratinginfo.exists():
                modelobj2 = PlaceRatings(
                    user_info=request.user,
                    place_name=cityname,
                    place_ratings=rating
                )
                modelobj2.save()


            # This is to calculate and save total rating
            ratedplaces = PlaceRatings.objects.all()
            for info in ratedplaces:
                if cityname.lower() == info.place_name.lower():
                    rating_count += 1
                    rating_sum += info.place_ratings

            total_rating = rating_sum / rating_count
            print(total_rating)
            # print("Total Rating: ", total_rating)
            mobj = DestinationCityDetails.objects.filter(destination_name=cityname.upper()).update(city_rating=total_rating)

            for city in citydetails:
                if cityname.upper() == city.destination_name.upper():
                    form = UserCityForm()
                    messages.warning(request,
                                    f"The city {cityname} already exist, try with other city, your ratings if for the first time, will be noted!")
                    # return reverse_lazy('club:addCity')
                    return render(request, 'locapp/userCityForm.html', context={'form': form})
            if form.is_valid():
                modelobj = DestinationCityDetails(
                    # destination_name=form.cleaned_data['destination_name'],
                    destination_name=cityname.upper(),
                    destinationImage=form.cleaned_data['destinationImage'],
                    destination_desc=form.cleaned_data['destination_desc'],
                    # destination_extras=form.cleaned_data['destination_extras'],
                    city_rating=total_rating
                )
                # form.save(commit=False)
                # form.city_rating = rating
                modelobj.save()

                messages.info(request, "Your city information has been sent for the approval!")
                # form.save()
        form = UserCityForm()
        return render(request, 'locapp/userCityForm.html', context={'form': form})
    else:
        messages.info(request,"You need to login to avail this option!")
        return redirect('locapp:dest')


def userplaceform(request):
    if request.user.is_authenticated:
        rating_count = 0
        rating_sum = 0
        place_details = DestinationMetaDetails.objects.all()
        print(request.user)
        if request.method == 'POST':
            form = UserPlaceForm(request.POST, request.FILES)
            placename = request.POST.get('meta_destination_name')
            placename = placename.upper()
            print(placename)
            rating = request.POST.get('rating')
            placeratinginfo = PlaceRatings.objects.filter(user_info=request.user, place_name=placename)
            if not placeratinginfo.exists():
                modelobj2 = PlaceRatings(
                    user_info=request.user,
                    place_name=placename,
                    place_ratings=rating
                )
                modelobj2.save()

            ratedplaces = PlaceRatings.objects.all()
            for info in ratedplaces:
                if placename.lower() == info.place_name.lower():
                    rating_count += 1
                    rating_sum += info.place_ratings
            total_rating = rating_sum / rating_count
            mobj = DestinationMetaDetails.objects.filter(meta_destination_name=placename.upper()).update(
                place_rating=total_rating)
            for place in place_details:
                if placename.upper() == place.meta_destination_name.upper():
                    form = UserPlaceForm()
                    messages.warning(request,
                                    f"The place {placename} already exist, your ratings if for the first time, will be noted!!")
                    return render(request, 'locapp/userPlaceForm.html', context={'form': form})
            if form.is_valid():
                modelobj = DestinationMetaDetails(
                    meta_destination=form.cleaned_data['meta_destination'],
                    meta_destination_name=placename.upper(),
                    meta_destination_Image=form.cleaned_data['meta_destination_Image'],
                    meta_destination_desc=form.cleaned_data['meta_destination_desc'],
                    destination_extras=form.cleaned_data['destination_extras'],
                    place_rating=total_rating
                )
                modelobj.save()

                messages.info(request, "Your city information has been sent for the approval!")
        form = UserPlaceForm()
        return render(request, 'locapp/userPlaceForm.html', context={'form': form})
    else:
        messages.info(request,"You need to login to avail this option!")
        return redirect('locapp:dest')

def aboutUs(request):
    context={}
    return render(request,'locapp/about.html',context)


def direct_rating(request):
    if request.user.is_authenticated:
        rating_count = 0
        rating_sum = 0
        form = PlaceRatingForm()
        if request.method == "POST":
            form = PlaceRatingForm(request.POST)
            rating = request.POST.get('rating')
            mydestination = request.POST.get("place_name")
            placeratinginfo = PlaceRatings.objects.filter(user_info=request.user, place_name=mydestination.upper())
            if not placeratinginfo.exists():
                mymodelobj = PlaceRatings(
                    user_info=request.user,
                    place_name=mydestination.upper(),
                    place_ratings=rating
                )
                mymodelobj.save()
                # messages.success(request,f'The destination {mydestination} rating has been saved!')
                # return reverse_lazy('locapp:dest')
            else:
                messages.warning(request, f"{request.user}, You've already rated the destination!")
                form = PlaceRatingForm()
                return render(request, 'locapp/directuserrating.html', context={'form': form})
            ratedplaces = PlaceRatings.objects.all()
            for info in ratedplaces:
                if mydestination.lower() == info.place_name.lower():
                    rating_count += 1
                    rating_sum += info.place_ratings
            total_rating = rating_sum / rating_count
            DestinationCityDetails.objects.filter(destination_name=mydestination.upper()).update(city_rating=total_rating)
            DestinationMetaDetails.objects.filter(meta_destination_name=mydestination.upper()).update(
                place_rating=total_rating)
            messages.success(request, f"The destination {mydestination} rating has been saved! we'll utilize your ratings if city/place is authentic!")
            form = PlaceRatingForm()

        return render(request, 'locapp/directuserrating.html', context={'form': form})
    else:
        messages.info(request,"You need to login to rate the City or a Place!")
        return redirect('locapp:dest')

def Blog(request,key):
    context={'key':key}
    return render(request,'locapp/blog.html',context)

def search(request):
    search=[]
    search_recv = request.GET.get('term')
    print(request.GET)
    search_results = DestinationCityDetails.objects.filter(destination_name__icontains=search_recv)
    for result in search_results:
        search.append(result.destination_name)
    return JsonResponse(search, safe=False)
