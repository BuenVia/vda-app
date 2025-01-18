from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .forms import ToolEquipmentForm, CalibrationTestForm
from .models import ToolEquipment, CalibrationTest
from clients.models import Client
from vda.views import is_admin


@login_required
@user_passes_test(is_admin)
def create_tool_equipment(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        form = ToolEquipmentForm(request.POST)
        if form.is_valid():
            tool_equipment = form.save(commit=False)
            tool_equipment.client = client
            tool_equipment.save()
            messages.success(request, "Tool/Equipment added successfully!")
            return redirect('client_detail', client_id=client.id)
        else:
            messages.error(request, "Error adding tool/equipment. Please try again.")
    else:
        form = ToolEquipmentForm()

    return render(request, 'tools/create_tool_equipment.html', {'form': form, 'client': client})

@login_required
# @user_passes_test(is_admin)
def equipment_detail(request, equipment_id):
    equipment = get_object_or_404(ToolEquipment, id=equipment_id)
    return render(request, 'tools/equipment_detail.html', {'equipment': equipment})

@login_required
@user_passes_test(is_admin)
def edit_or_delete_equipment(request, equipment_id):
    equipment = get_object_or_404(ToolEquipment, id=equipment_id)
    client = equipment.client
    if request.method == 'POST':
        if 'update' in request.POST:  # Handle update
            form = ToolEquipmentForm(request.POST, instance=equipment)
            if form.is_valid():
                form.save()
                messages.success(request, "Equipment updated successfully!")
                return redirect('equipment_detail', equipment_id=equipment.id)
        elif 'delete' in request.POST:  # Handle delete
            equipment.delete()
            messages.success(request, "Equipment deleted successfully!")
            return redirect('client_detail', client_id=client.id)
    else:
        form = ToolEquipmentForm(instance=equipment)

    return render(request, 'tools/edit_or_delete_equipment.html', {'form': form, 'equipment': equipment})

@login_required
def client_tool_equipment_list(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    tools = client.tools_equipment.all()  # Adjust related name if necessary

    return render(
        request,
        'tools/tool_list.html',
        {
            'client': client,
            'tools': tools,
        }
    )

@login_required
@user_passes_test(is_admin)
def create_calibration_test(request, equipment_id):
    equipment = get_object_or_404(ToolEquipment, id=equipment_id)
    client = equipment.client
    if request.method == 'POST':
        form = CalibrationTestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.equipment = equipment
            test.client = client
            test.save()
            messages.success(request, f"Calibration Test '{test.test_name}' added successfully!")
            return redirect('equipment_detail', equipment_id=equipment.id)
        else:
            messages.error(request, "Error adding calibration test. Please try again.")
    else:
        form = CalibrationTestForm()

    return render(request, 'tools/create_calibration_test.html', {'form': form, 'equipment': equipment})

@login_required
@user_passes_test(is_admin)
def edit_or_delete_calibration_test(request, test_id):
    test = get_object_or_404(CalibrationTest, id=test_id)
    equipment = test.equipment
    if request.method == 'POST':
        if 'update' in request.POST:  # Handle update
            form = CalibrationTestForm(request.POST, instance=test)
            if form.is_valid():
                form.save()
                messages.success(request, f"Calibration Test '{test.test_name}' updated successfully!")
                return redirect('equipment_detail', equipment_id=equipment.id)
        elif 'delete' in request.POST:  # Handle delete
            test.delete()
            messages.success(request, f"Calibration Test '{test.test_name}' deleted successfully!")
            return redirect('equipment_detail', equipment_id=equipment.id)
    else:
        form = CalibrationTestForm(instance=test)

    return render(request, 'tools/edit_or_delete_calibration_test.html', {'form': form, 'test': test, 'equipment': equipment})