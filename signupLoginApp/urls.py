from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login', views.user_login, name='login'),
    path('doctor_dashboard', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient_dashboard', views.patient_dashboard, name='patient_dashboard'),
    path('logout', views.logoutPage, name='logout'),
]