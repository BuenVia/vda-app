from django.urls import path

from . import views

urlpatterns = [
        path('client/<int:client_id>/tools/', views.client_tool_equipment_list, name='client_tool_equipment_list'),
        path('client/<int:client_id>/add-tool-equipment/', views.create_tool_equipment, name='create_tool_equipment'),
        path('equipment/<int:equipment_id>/', views.equipment_detail, name='equipment_detail'),
        path('equipment/<int:equipment_id>/edit/', views.edit_or_delete_equipment, name='edit_or_delete_equipment'),
        path('equipment/<int:equipment_id>/add-test/', views.create_calibration_test, name='create_calibration_test'),
        path('test/<int:test_id>/edit/', views.edit_or_delete_calibration_test, name='edit_or_delete_calibration_test'),
]
