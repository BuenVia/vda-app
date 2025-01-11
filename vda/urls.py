from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('create-client/', views.create_client, name='create_client'),
    path('clients/', views.client_list, name='client_list'),
    path('create-user/', views.create_user, name='create_user'),
    path('client/<int:client_id>/', views.client_detail, name='client_detail'),
    path('client/<int:client_id>/add-staff/', views.create_staff, name='create_staff'),
    path('staff/<int:staff_id>/', views.staff_profile, name='staff_profile'),
    path('staff/<int:staff_id>/edit/', views.edit_or_delete_staff, name='edit_or_delete_staff'),
    path('staff/<int:staff_id>/add-job/', views.create_job, name='create_job'),
    path('job/<int:job_id>/edit/', views.edit_or_delete_job, name='edit_or_delete_job'),
    path('staff/<int:staff_id>/add-qualification/', views.create_qualification, name='create_qualification'),
    path('qualification/<int:qualification_id>/edit/', views.edit_or_delete_qualification, name='edit_or_delete_qualification'),


]