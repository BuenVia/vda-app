from django.urls import path

from . import views
urlpatterns = [
    path('create-client/', views.create_client, name='create_client'),
    path('clients/', views.client_list, name='client_list'),
    path('create-user/', views.create_user, name='create_user'),
    path('client/<int:client_id>/', views.client_detail, name='client_detail'),
    path('update-user/', views.update_user, name='update_user'),
    path('users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/edit/', views.edit_or_delete_user, name='edit_or_delete_user'),
]