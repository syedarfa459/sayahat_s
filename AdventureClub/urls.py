from django.conf import settings
from django.urls import path
from . import views
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name="club"

urlpatterns = [
    # path('', views.home),
    path('', views.index, name='index'),

    # urls for user login/register/logout
    path('register/', views.RegisterClub, name='register'),
    path('signUp/', views.signup, name='signUp'),
    path('signOut/', views.signOut, name='signOut'),
    path('signIn/', views.signIn, name='signIn'),
    path('createEvent/',views.createEvent,name="createEvent"),
    path('myClubs/',views.myClubs,name="myClubs"),
    path('onGoingEvents/',views.onGoingEvents,name="events"),
    path('searchResults/',views.searchResults,name="searchResults"),
    path('detail/<int:pk>/',views.clubDetail,name="detail"),
    path('deleteClub/<int:pk>/',views.deleteClub.as_view(),name='deleteClub'),
    path('updateClub/<int:pk>/',views.updateClub.as_view(),name='updateClub'),
    path('popEvent/<int:pk>/',views.popedEvent,name='popEvent'),
    path('eventDetails/<int:pk>/',views.eventDetails.as_view(),name='eventDetails'),



]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)