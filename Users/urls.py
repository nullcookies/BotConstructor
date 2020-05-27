from django.urls import path

from .views import *

urlpatterns = [
    path('', base_view, name='base_view_url'),
    path('signup/', UserRegistration.as_view(), name='user_registration_url'),
    path(
        'login/', UserAuthentication.as_view(), name='user_authentication_url'
    ),
    path(
        'update-profile/', UpdateProfile.as_view(), name='update_profile_url'
    ),
    path('profile/', ProfileView.as_view(), name='profile_url'),
    path('logout', UserLogout.as_view(), name='user_logout_url'),
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate')
]
