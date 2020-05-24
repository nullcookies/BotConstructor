from django.urls import path

from .views import *

urlpatterns = [
    path('', base_view, name='base_view_url'),
    path('signUp/', UserRegistration.as_view(), name='user_registration_url'),
    path('signIn/', UserAuthentication.as_view(),
         name='user_authentication_url'),
    path('updateProfile/', UpdateProfile.as_view(), name='update_profile_url'),
    path('profile/', ProfileView.as_view(), name='profile_url'),
    path('logOut', UserLogout.as_view(), name='user_logout_url'),
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate')
]
