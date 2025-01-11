from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .forms import ClientForm, UserForm, StaffForm, JobForm, QualificationForm
from .models import Client, Staff, Job, Qualification

def index(request):
    return render(request, 'index.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('login')


# Check if the user is an admin
def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client created successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Error creating client. Please check the form and try again.')
    else:
        form = ClientForm()

    return render(request, 'create_client.html', {'form': form})


@user_passes_test(is_admin)
def client_list(request):
    clients = Client.objects.all()
    return render(request, 'client_list.html', {'clients': clients})


@user_passes_test(is_admin)
def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['username']  # Set the username
            user.set_password(form.cleaned_data['password'])  # Set the password securely
            user.save()
            messages.success(request, f"User {user.first_name} {user.last_name} created successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "Error creating user. Please check the form and try again.")
    else:
        form = UserForm()

    return render(request, 'create_user.html', {'form': form})


def client_detail(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    users = client.user_set.all()  # Retrieve associated users
    staff_members = client.staff.all()  # Retrieve associated staff
    return render(request, 'client_detail.html', {'client': client, 'users': users, 'staff_members': staff_members})


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

    return render(request, 'create_staff.html', {'form': form, 'client': client})

def staff_profile(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    return render(request, 'staff_profile.html', {'staff': staff})

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

    return render(request, 'edit_or_delete_staff.html', {'form': form, 'staff': staff})



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
            return redirect('staff_profile', staff_id=staff.id)
        else:
            messages.error(request, "Error adding job. Please try again.")
    else:
        form = JobForm()

    return render(request, 'create_job.html', {'form': form, 'staff': staff, 'client': client})


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
                return redirect('staff_profile', staff_id=staff.id)
        elif 'delete' in request.POST:
            job.delete()
            messages.success(request, "Job deleted successfully!")
            return redirect('staff_profile', staff_id=staff.id)
    else:
        form = JobForm(instance=job)

    return render(request, 'edit_or_delete_job.html', {'form': form, 'job': job, 'staff': staff})


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
            return redirect('staff_profile', staff_id=staff.id)
        else:
            messages.error(request, "Error adding qualification. Please try again.")
    else:
        form = QualificationForm()
        form.fields['job'].queryset = jobs  # Limit jobs to those linked to the staff member

    return render(request, 'create_qualification.html', {'form': form, 'staff': staff})


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
                return redirect('staff_profile', staff_id=staff.id)
        elif 'delete' in request.POST:
            qualification.delete()
            messages.success(request, f"Qualification '{qualification.name}' deleted successfully!")
            return redirect('staff_profile', staff_id=staff.id)
    else:
        form = QualificationForm(instance=qualification)
        form.fields['job'].queryset = staff.jobs.all()

    return render(request, 'edit_or_delete_qualification.html', {'form': form, 'qualification': qualification, 'staff': staff})
