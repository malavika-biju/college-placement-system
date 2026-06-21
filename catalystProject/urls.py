from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static


def home(request):
    return redirect('guest_home')   # Redirect to your guest home page


urlpatterns = [
    path('', home, name='home'),

    path('admin/', admin.site.urls),

    path('adminapp/', include('adminapp.adminurls')),
    path('guestapp/', include('guestapp.guesturls')),
    path('companyapp/', include('companyapp.companyurls')),
    path('studentapp/', include('studentapp.studenturls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
