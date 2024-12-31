from django.urls import path
from .views import home, select_seat, confirmation
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', home, name='home'),
    path('select-seat/', select_seat, name='select_seat'),
    path('confirmation/', confirmation, name='confirmation'),
    path('get_destinations/', views.get_destinations, name='get_destinations'),
    path('login/', LoginView.as_view(template_name='bookings/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.register, name='register'),
    path('otp-login/', views.otp_login, name='otp_login'),
]
