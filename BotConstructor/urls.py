from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Users.urls')),
    path('', include('Bots.urls'))
] + static(settings.MEDIA_URL, document=settings.MEDIA_ROOT)
