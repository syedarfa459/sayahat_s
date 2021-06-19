from django.db import models

# Create your models here.

class Tourist(models.Model):

    tourist_name = models.CharField(max_length = 30)
    tourist_latitude = models.FloatField(null = True)
    tourist_longitude = models.FloatField(null = True)
    tourist_location = models.CharField(max_length = 50)

    def __str__(self):
        return self.tourist_name + self.tourist_location

class Destination(models.Model):

    destination = models.CharField(max_length = 150)
    distance = models.DecimalField(max_digits = 10, decimal_places = 2)
    dated = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"Distance from TouristLocation to {self.destination} is {self.distance} km"

class DestinationCityDetails(models.Model):

    destination_name = models.CharField(max_length=50)
    destinationImage = models.ImageField(upload_to='destinationImages', blank = True, null = True)
    destination_desc = models.TextField()
    # destination_extras = models.CharField(max_length=200)
    city_rating = models.PositiveIntegerField()
    admin_approved=models.BooleanField(default=False,blank=True,null=True)

    def __str__(self):

        return self.destination_name

class DestinationMetaDetails(models.Model):

    meta_destination = models.ForeignKey(DestinationCityDetails, models.CASCADE)
    meta_destination_name = models.CharField(max_length=60)
    meta_destination_Image = models.ImageField(upload_to='metadestinationImages')
    meta_destination_desc = models.TextField()
    destination_extras = models.CharField(max_length=200)
    place_rating = models.PositiveIntegerField()
    admin_approved=models.BooleanField(default=False,blank=True,null=True)


    def __str__(self):

        return self.meta_destination_name + " " + self.meta_destination.destination_name

class PlaceRatings(models.Model):
    user_info = models.CharField(max_length=25)
    place_name = models.CharField(max_length=60)
    place_ratings = models.PositiveIntegerField()

    def __str__(self):
        return self.user_info + " " + self.place_name + " " + str(self.place_ratings)