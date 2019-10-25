from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<str:username>/', views.profile, name='profile'),
    # path('item/<int:item_id>/', views.item, name='item'),
    path('item/', views.item, name='item'), # For debugging purposes only. Once it works start making items to check functionality
    path('login/', views.login, name='login'),
]