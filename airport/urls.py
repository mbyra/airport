from django.urls import path, re_path

from . import views

app_name = 'airport'
urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('flight/<int:flight_no>/', views.flight_details, name='flight_details'),
    path('login_or_register/', views.login_or_register, name='login_or_register'),
    path('registration_form/', views.registration_form, name='registration_form'),
    path('register/', views.register, name='register'),
    path('buy_ticket/<int:flight_no>/', views.buy_ticket, name='buy_ticket'),
    path('logout/', views.logout_view, name='logout_view'),
    path('crew/login/', views.crew_login, name='crew_login'),
    path('crew/get_flight_and_crew_lists/', views.get_flight_and_crew_lists, name='get_flight_and_crew_lists'),
    path('crew/assign_crew/', views.assign_crew, name='assign_crew'),

]
