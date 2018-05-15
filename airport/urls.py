from django.urls import path, re_path

from . import views

app_name = 'airport'
urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('flight/<int:flight_no>/', views.flight_details, name='flight_details'),
    path('login_or_register/', views.login_or_register, name='login_or_register'),
    path('logout/', views.logout_view, name='logout_view'),
    # path('account/', views.account, name='account'),
]
