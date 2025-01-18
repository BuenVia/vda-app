from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),
    # path('create-client/', views.create_client, name='create_client'),
    # path('clients/', views.client_list, name='client_list'),
    # path('create-user/', views.create_user, name='create_user'),
    # path('client/<int:client_id>/', views.client_detail, name='client_detail'),
    # path('update-user/', views.update_user, name='update_user'),
    # path('users/', views.user_list, name='user_list'),
    # path('users/<int:user_id>/edit/', views.edit_or_delete_user, name='edit_or_delete_user'),
]

# from django.conf.urls import handler404, handler403
# from .views import custom_permission_denied_view

# handler404 = 'django.views.defaults.page_not_found'
# handler403 = 'myapp.views.custom_permission_denied_view'
