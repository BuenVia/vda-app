from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .forms import StaffForm, JobForm, QualificationForm
from .models import Staff, Job, Qualification
from clients.models import Client
from vda.views import is_admin


# STAFF
@login_required
def client_staff_list(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    staff_members = client.staff.all()  # Adjust related name if necessary

    return render(
        request,
        'staff/list_staff.html',
        {
            'client': client,
            'staff_members': staff_members,
        }
    )

@login_required
@user_passes_test(is_admin)
def create_staff(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            staff = form.save(commit=False)
            staff.client = client
            staff.save()
            messages.success(request, f"Staff member {staff.first_name} {staff.last_name} added successfully!")
            return redirect('client_detail', client_id=client.id)
        else:
            messages.error(request, "Error adding staff member. Please check the form and try again.")
    else:
        form = StaffForm()

    return render(request, 'staff/create_staff.html', {'form': form, 'client': client})

@login_required
def read_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    return render(request, 'staff/read_staff.html', {'staff': staff})

@user_passes_test(is_admin)
def edit_or_delete_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    if request.method == 'POST':
        if 'update' in request.POST:  # Handle update
            form = StaffForm(request.POST, instance=staff)
            if form.is_valid():
                form.save()
                messages.success(request, "Staff member updated successfully!")
                return redirect('client_detail', client_id=staff.client.id)
        elif 'delete' in request.POST:  # Handle delete
            client_id = staff.client.id
            staff.delete()
            messages.success(request, "Staff member deleted successfully!")
            return redirect('client_detail', client_id=client_id)
    else:
        form = StaffForm(instance=staff)

    return render(request, 'staff/edit_or_delete_staff.html', {'form': form, 'staff': staff})

# JOB
@login_required
@user_passes_test(is_admin)
def create_job(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    client = staff.client  # Derive the client from the staff member
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.staff = staff
            job.client = client
            job.save()
            messages.success(request, f"Job {job.role} added for {staff.first_name} {staff.last_name}!")
            return redirect('read_staff', staff_id=staff.id)
        else:
            messages.error(request, "Error adding job. Please try again.")
    else:
        form = JobForm()

    return render(request, 'staff/create_job.html', {'form': form, 'staff': staff, 'client': client})

@login_required
@user_passes_test(is_admin)
def edit_or_delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    staff = job.staff
    if request.method == 'POST':
        if 'update' in request.POST:
            form = JobForm(request.POST, instance=job)
            if form.is_valid():
                form.save()
                messages.success(request, f"Job {job.role} updated successfully!")
                return redirect('read_staff', staff_id=staff.id)
        elif 'delete' in request.POST:
            job.delete()
            messages.success(request, "Job deleted successfully!")
            return redirect('read_staff', staff_id=staff.id)
    else:
        form = JobForm(instance=job)

    return render(request, 'staff/edit_or_delete_job.html', {'form': form, 'job': job, 'staff': staff})

# QUALIFICATION
@login_required
@user_passes_test(is_admin)
def create_qualification(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    jobs = staff.jobs.all()  # Get jobs associated with this staff member
    if request.method == 'POST':
        form = QualificationForm(request.POST)
        form.fields['job'].queryset = jobs  # Limit jobs to those linked to the staff member
        if form.is_valid():
            qualification = form.save()
            messages.success(request, f"Qualification '{qualification.name}' added successfully!")
            return redirect('read_staff', staff_id=staff.id)
        else:
            messages.error(request, "Error adding qualification. Please try again.")
    else:
        form = QualificationForm()
        form.fields['job'].queryset = jobs  # Limit jobs to those linked to the staff member

    return render(request, 'staff/create_qualification.html', {'form': form, 'staff': staff})

@login_required
@user_passes_test(is_admin)
def edit_or_delete_qualification(request, qualification_id):
    qualification = get_object_or_404(Qualification, id=qualification_id)
    staff = qualification.job.staff
    if request.method == 'POST':
        if 'update' in request.POST:
            form = QualificationForm(request.POST, instance=qualification)
            form.fields['job'].queryset = staff.jobs.all()  # Limit jobs to staff's jobs
            if form.is_valid():
                form.save()
                messages.success(request, f"Qualification '{qualification.name}' updated successfully!")
                return redirect('read_staff', staff_id=staff.id)
        elif 'delete' in request.POST:
            qualification.delete()
            messages.success(request, f"Qualification '{qualification.name}' deleted successfully!")
            return redirect('read_staff', staff_id=staff.id)
    else:
        form = QualificationForm(instance=qualification)
        form.fields['job'].queryset = staff.jobs.all()

    return render(request, 'staff/edit_or_delete_qualification.html', {'form': form, 'qualification': qualification, 'staff': staff})


@login_required
def competency(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    qualifications = Qualification.objects.filter(job__staff__client=client).select_related('job', 'job__staff')

    return render(
        request,
        'staff/competency.html',
        {
            'client': client,
            'qualifications': qualifications,
        }
    )

