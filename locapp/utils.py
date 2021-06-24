# from django.contrib.gis.geoip2 import GeoIP2
from collections import namedtuple
from .models import Destination, Tourist, DestinationCityDetails, DestinationMetaDetails
import folium
from geopy.geocoders import Nominatim
import socket
import geocoder
from geopy.distance import geodesic
import requests
import json
from ipregistry import IpregistryClient


#creating my project helper functions here

def get_center_coordinates(latA, longA, latB=None, longB=None):
    cord = (latA, longA)
    if latB:
        cord = [(latA+latB)/2, (longA+longB)/2]
    return cord

def get_zoom(distance):

    if distance <=20:
        return 12
    elif distance<=50:
        return 10
    elif distance <= 100:
        return 9
    elif distance > 100 and distance <= 1500:
        return 5
    elif distance > 1501 and distance <= 3000:
        return 4
    else:
        return 2


def location_module(destination_,u_ip):

    city=destination_
    geolocator = Nominatim(user_agent='syedarfa')

    client = IpregistryClient("escffgkb0orli5")
    ipInfo = client.lookup()
    
#     hostname= socket.gethostname()
#     local_ip = socket.gethostbyname(hostname)
    local_ip= u_ip
    
    response = requests.get("http://ip-api.com/json/",local_ip).json()
    mylatitude= response['lat']
    mylongitude= response['lon']
    # print(ipInfo)
    # print(ipInfo.ip)
    # print(ipInfo.location.get('latitude'))
    # print(ipInfo.location.get('longitude'))
#     mylatitude = ipInfo.location.get('latitude')
#     mylongitude = ipInfo.location.get('longitude')
    mycity = ipInfo.location.get('city')

    tourist_lat, tourist_lon = mylatitude, mylongitude

    print("yahan", tourist_lat)
    touristLocation = (tourist_lat, tourist_lon)
    # to get the location details of the tourist
    touristlocdetails = geolocator.reverse(str(tourist_lat) + ',' + str(tourist_lon))
    touristaddress = touristlocdetails.raw['address']
    # print(touristaddress)
    tourist_state = touristaddress.get('state', '')
    tourist_country = touristaddress.get('country', '')
    tourist_locdetails = tourist_state + tourist_country
    # print('Details are ' + tourist_locdetails)

    # Map using folium library
    # the map will point to the location of tourist
    mapobj = folium.Map(width=380, height=600, location=touristLocation, zoom_start=15)
    # adding marker at tourist location
    folium.Marker([tourist_lat, tourist_lon], tooltip='Click to get the name of city', popup=mycity,
                  icon=folium.Icon(color='green')).add_to(mapobj)

    
    if geolocator.geocode(destination_) is None:
        return "not found"
    # print(destination.address)
    # print(destination.latitude)
    # if not destination.latitude:
    else:
        destination = geolocator.geocode(destination_)
        dest_lat = destination.latitude
        # print(destination.longitude)
        dest_long = destination.longitude

        destinationLocation = (dest_lat, dest_long)

        # Now calculating the distance between tourist location and distance location
        distance = geodesic(touristLocation, destinationLocation).km

        # Now to plot the route between tourist location and the destination
        mapobj = folium.Map(width=550, height=380,
                            location=get_center_coordinates(tourist_lat, tourist_lon, dest_lat, dest_long),
                            zoom_start=get_zoom(distance))
        # TouristLocation
        folium.Marker([tourist_lat, tourist_lon], tooltip='Click to get the name of city', popup=mycity,
                    icon=folium.Icon(color='green')).add_to(mapobj)
        # TouristDestination
        folium.Marker([dest_lat, dest_long], tooltip='Click to get the name of city', popup=destination,
                    icon=folium.Icon(color='blue')).add_to(mapobj)
        # Now we will draw line between touristlocation and tourist destination
        line = folium.PolyLine(locations=[touristLocation, destinationLocation], weight=2.5, color='red')
        # adding the line to our map now
        mapobj.add_child(line)
        mapobj = mapobj._repr_html_()
        dest_meta_details = DestinationMetaDetails.objects.filter(meta_destination__in=DestinationCityDetails.objects.filter(destination_name__icontains=city))
        # print("--------------------------------------,",dest_meta_details)
        # print("destttttttttttttttttttt===", dest_meta_details)
        return [distance,mapobj,dest_meta_details,tourist_lat,tourist_lon,tourist_locdetails,dest_lat,dest_long]
