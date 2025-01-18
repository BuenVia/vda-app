from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .forms import ClientForm, UserForm, UserUpdateForm
from .models import Client, User
from documents.enums import DocumentCategory
from documents.models import Document
from staff.models import Staff
from vda.views import is_admin


# Create your views here.
@login_required
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

    return render(request, 'clients/create_client.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def client_list(request):
    clients = Client.objects.all()
    return render(request, 'clients/client_list.html', {'clients': clients})

@login_required
@user_passes_test(is_admin)
def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['username']  # Set the username
            user.set_password(form.cleaned_data['password'])  # Set the password securely
            user.save()
            # messages.success(request, f"User {user.first_name} {user.last_name} created successfully!")
            messages.success(request, f"User {user.first_name} {user.last_name} created successfully!", extra_tags='user_creation')
            return redirect('dashboard')
        else:
            messages.error(request, "Error creating user. Please check the form and try again.", extra_tags='user_creation_error')
            # messages.error(request, "Error creating user. Please check the form and try again.")

    else:
        form = UserForm()

    return render(request, 'clients/create_user.html', {'form': form})

@login_required
def client_detail(request, client_id):
    if request.user.client_id == client_id or request.user.is_superuser:
        client = get_object_or_404(Client, id=client_id)
        users = client.user_set.all()  # Retrieve associated users
        # jobs = client.jobs.all().select_related('staff')  # Retrieve associated jobs with staff
        # if len(jobs) < 1:
        staff_members = Staff.objects.filter(client_id=client_id).all()
        # else:
        #     staff_members = {job.staff for job in jobs}  # Get unique staff members from jobs
        tools_equipment = client.tools_equipment.all()  # Retrieve tools and equipment
        documents = Document.objects.filter(client=client)
        document_status = {category.name: None for category in DocumentCategory}

        for doc in documents:
            document_status[doc.category] = doc

        return render(
            request,
            'clients/client_detail.html',
            {
                'client': client,
                'users': users,
                'staff_members': staff_members,
                'tools_equipment': tools_equipment,
                'document_status': document_status,
            }
        )
    else:
        return render(request, '404.html')

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

    return render(request, 'clients/update_user.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def user_list(request):
    users = User.objects.select_related('client').all()  # Assuming User has a foreign key to Client
    return render(request, 'clients/user_list.html', {'users': users})

@login_required
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

    return render(request, 'clients/edit_or_delete_user.html', {'form': form, 'user': user})
