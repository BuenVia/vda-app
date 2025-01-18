from django.urls import path

from . import views

urlpatterns = [
    path('client/<int:client_id>/documents/', views.document_list, name='document_list'),
    path('client/<int:client_id>/upload/<str:category>/', views.upload_document, name='upload_document'),
    path('document/<int:document_id>/delete/', views.delete_document, name='delete_document'),
]