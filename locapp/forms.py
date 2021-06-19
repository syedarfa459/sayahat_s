from django import forms
from .models import Destination, Tourist, DestinationMetaDetails, DestinationCityDetails, PlaceRatings

class DestinationForm(forms.ModelForm):
    destination=forms.CharField(widget= forms.TextInput
                           (attrs={'placeholder':'Enter Name of City'}),label='')
    class Meta:
        model = Destination
        fields = ('destination',)

class TouristForm(forms.ModelForm):

    class Meta:
        model = Tourist
        fields = ('tourist_name','tourist_latitude','tourist_longitude','tourist_location')

class UserCityForm(forms.ModelForm):
    destination_desc= forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":10}))
    
    class Meta:
        model = DestinationCityDetails
        fields = ('destination_name','destinationImage','destination_desc')
        

class UserPlaceForm(forms.ModelForm):
    meta_destination_desc= forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":10}))
    class Meta:
        model = DestinationMetaDetails
        fields = ('meta_destination','meta_destination_name','meta_destination_Image','meta_destination_desc','destination_extras')


class PlaceRatingForm(forms.ModelForm):
    class Meta:
        model = PlaceRatings
        fields = ('place_name',)