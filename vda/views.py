from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from .forms import ClientForm, UserForm, StaffForm, JobForm, QualificationForm, ToolEquipmentForm, CalibrationTestForm, DocumentUploadForm, UserUpdateForm
from .models import Client, Staff, Job, Qualification, ToolEquipment, CalibrationTest, Document, User
from .enums import DocumentCategory


# def index(request):
#     return render(request, 'index.html')

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

# def custom_permission_denied_view(request, exception=None):
#     return render(request, '404.html', status=404)

@login_required
def dashboard(request):
    if request.user.is_superuser:
        clients = Client.objects.annotate(staff_count=Count('staff'))
        total_clients = clients.count()

        return render(
            request,
            'admin_dashboard.html',
            {
                'total_clients': total_clients,
                'clients': clients,
            }
        )

    # Standard user dashboard
    client = request.user.client  # Assuming `client` is a ForeignKey on the User model
    staff_count = Staff.objects.filter(client=client).count()
    equipment_count = ToolEquipment.objects.filter(client=client).count()
    document_count = Document.objects.filter(client=client).count()

    return render(
        request,
        'user_dashboard.html',
        {
            'client': client,
            'user': request.user,
            'staff_count': staff_count,
            'equipment_count': equipment_count,
            'document_count': document_count,
        }
    )

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('login')


# Check if the user is an admin
def is_admin(user):
    print(f"User: {user.username}, Is Superuser: {user.is_superuser}")
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
    jobs = client.jobs.all().select_related('staff')  # Retrieve associated jobs with staff
    staff_members = {job.staff for job in jobs}  # Get unique staff members from jobs
    tools_equipment = client.tools_equipment.all()  # Retrieve tools and equipment
    documents = Document.objects.filter(client=client)
    document_status = {category.name: None for category in DocumentCategory}

    for doc in documents:
        document_status[doc.category] = doc

    return render(
        request,
        'client_detail.html',
        {
            'client': client,
            'users': users,
            'staff_members': staff_members,
            'tools_equipment': tools_equipment,
            'document_status': document_status,
        }
    )



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



# @user_passes_test(is_admin)
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


# @user_passes_test(is_admin)
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


# @user_passes_test(is_admin)
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



def competency(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    qualifications = Qualification.objects.filter(job__staff__client=client).select_related('job', 'job__staff')

    return render(
        request,
        'competency.html',
        {
            'client': client,
            'qualifications': qualifications,
        }
    )



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

    return render(request, 'create_tool_equipment.html', {'form': form, 'client': client})

# @user_passes_test(is_admin)
def equipment_detail(request, equipment_id):
    equipment = get_object_or_404(ToolEquipment, id=equipment_id)
    return render(request, 'equipment_detail.html', {'equipment': equipment})

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

    return render(request, 'edit_or_delete_equipment.html', {'form': form, 'equipment': equipment})


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

    return render(request, 'create_calibration_test.html', {'form': form, 'equipment': equipment})


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

    return render(request, 'edit_or_delete_calibration_test.html', {'form': form, 'test': test, 'equipment': equipment})


# @user_passes_test(is_admin)
def document_list(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    documents = Document.objects.filter(client=client)
    document_status = {category.name: None for category in DocumentCategory}
    
    for doc in documents:
        document_status[doc.category] = doc
    
    return render(request, 'document_list.html', {'client': client, 'document_status': document_status})

# @user_passes_test(is_admin)
def upload_document(request, client_id, category):
    client = get_object_or_404(Client, id=client_id)
    document, created = Document.objects.get_or_create(client=client, category=category)

    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            document = form.save(commit=False)
            document.upload_date = timezone.now()
            document.save()
            messages.success(request, f"Document '{document.get_category_display()}' uploaded successfully!")
            return redirect('client_detail', client_id=client.id)
        else:
            messages.error(request, "Error uploading document. Please try again.")
    else:
        form = DocumentUploadForm(instance=document)

    return render(request, 'upload_document.html', {'form': form, 'client': client, 'category': category})


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

# @user_passes_test(lambda u: u.is_superuser)
def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    client_id = document.client.id  # Save client ID for redirecting
    document.delete()  # Delete the document
    messages.success(request, "Document deleted successfully!")
    return redirect('client_detail', client_id=client_id)


@login_required
def update_user(request):
    user = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserUpdateForm(instance=user)

    return render(request, 'update_user.html', {'form': form})


@user_passes_test(is_admin)
def user_list(request):
    users = User.objects.select_related('client').all()  # Assuming User has a foreign key to Client
    return render(request, 'user_list.html', {'users': users})

@user_passes_test(is_admin)
def edit_or_delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        if 'update' in request.POST:  # Handle update
            form = UserUpdateForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "User updated successfully!")
                return redirect('user_list')
            else:
                messages.error(request, "Error updating user. Please correct the form.")
        elif 'delete' in request.POST:  # Handle delete
            user.delete()
            messages.success(request, "User deleted successfully!")
            return redirect('user_list')
    else:
        form = UserUpdateForm(instance=user)

    return render(request, 'edit_or_delete_user.html', {'form': form, 'user': user})
