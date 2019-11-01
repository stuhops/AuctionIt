from django.urls import path

from . import views

app_name = 'auctions'
urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('profile/setup/', views.editProfile, name='editProfile'),
    path('item/<int:item_id>/', views.item, name='item'),
]
