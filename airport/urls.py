from django.urls import path, re_path

from . import views

app_name = 'airport'
urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('flight/<int:flight_no>', views.flight_details, name='flight_details'),
]