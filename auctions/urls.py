from django.urls import path

from . import views

app_name = 'auctions'
urlpatterns = [
    path('', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('item/<int:item_id>/', views.item, name='item'),
]
