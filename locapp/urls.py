from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

# from django.contrib.auth.decorators import login_required
app_name = 'locapp'

urlpatterns = [

    # path('', views.soclogin),
    path('', views.DestinationView, name='dest'),
    # path('tourist/', views.TouristView, name='tourist'),
    path('<int:pk>/', views.dest_view2, name="show_dest"),
    path('logout/', views.logoutuser, name='logout'),
    path('loc_meta_detail/<int:pk>', views.loc_meta_view, name="loc_meta_detail"),
    #     path('addDestination/',views.userDestForm.as_view(),name='addLoc'),
    #     path('addCity/',views.userCityForm.as_view(),name='addCity'),
    path('addCity/', views.usercityform, name='addCity'),
    #     path('addPlace/',views.userPlaceForm.as_view(),name='addPlace'),
    path('addPlace/', views.userplaceform, name='addPlace'),
    path('aboutUs/',views.aboutUs,name='aboutUs'),
    path('addRating/', views.direct_rating, name='addRating'),
    path('blog/<int:key>/',views.Blog,name='Blog'),

    path('searchsuggestion/', views.search, name='search'),

]
