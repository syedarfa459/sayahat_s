from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('locapp.urls')),
    path('/', include('AdventureClub.urls')),
    path('SayahatAdventure/', include('AdventureClub.urls')),
    path('accounts/', include('allauth.urls')),
    #for configuring media files on heroku
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),
    
    # urls for password reset at adventure club side
    # 1. for entering email to reset password
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='AdventureClubs/password_reset.html',
                                                                 email_template_name='AdventureClubs/myTemp.html'),
         name='password_reset'),

    # 2. for sending email to user who want to change password
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='AdventureClubs/password_reset_sent.html'),
         name='password_reset_done'),
    # urls for password reset
    # 3. The link from email on which user clicks to reset password
    path('lol/reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='AdventureClubs/password_reset_fill.html'),
         name='password_reset_confirm'),
    # 4. on successful reset of password
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='AdventureClubs/password_reset_complete.html'),
         name='password_reset_complete'),

]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
