from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'auctions'
urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('profile/setup/', views.editProfile, name='editProfile'),
    path('item/<int:item_pk>/', views.item, name='item'),
    path('codes', views.codes, name='codes'), 
    path('explore', views.explore, name='explore'),
    # path('join_auction/', views.join_auction, name='join_auction'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
