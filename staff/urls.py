from django.urls import path

from . import views
urlpatterns = [
    
    path('client/<int:client_id>/staff/', views.client_staff_list, name='list_staff'),
    path('client/<int:client_id>/add-staff/', views.create_staff, name='create_staff'),
    path('staff/<int:staff_id>/', views.read_staff, name='read_staff'),
    path('staff/<int:staff_id>/edit/', views.edit_or_delete_staff, name='edit_or_delete_staff'),
    path('staff/<int:staff_id>/add-job/', views.create_job, name='create_job'),
    path('job/<int:job_id>/edit/', views.edit_or_delete_job, name='edit_or_delete_job'),
    path('staff/<int:staff_id>/add-qualification/', views.create_qualification, name='create_qualification'),
    path('qualification/<int:qualification_id>/edit/', views.edit_or_delete_qualification, name='edit_or_delete_qualification'),
    path('client/<int:client_id>/competency/', views.competency, name='competency'),
]
