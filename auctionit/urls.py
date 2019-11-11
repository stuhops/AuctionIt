
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('auctions/', include('auctions.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('admin/', admin.site.urls),
]
