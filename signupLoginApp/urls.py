from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login', views.user_login, name='login'),
    path('doctor_dashboard', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient_dashboard', views.patient_dashboard, name='patient_dashboard'),
    path('logout', views.logoutPage, name='logout'),


    path('createPost', views.createPost_Page, name='createPost'),
    path('createCategory', views.createCategory_Page, name='createCategory'),
    path('blogList', views.blogList_Page, name='blogList'),
    path('blogDetail/<int:id>', views.blogDetail_Page, name='blogDetail'),
    path('storeDraft', views.storeDraft, name='storeDraft'),
    path('editDraft/<int:id>', views.editDraft, name='editDraft'),
    path('draftList', views.draftList, name='draftList'),
    
    path('doctorList', views.doctorList_Page, name='doctorList'),
    path('appointment/<int:id>', views.appointment_Page, name='appointment'),
    path('appointmntList', views.appointmntList_Page, name='appointmntList'),
]