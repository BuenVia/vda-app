from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from clients.models import Client, User
from documents.models import Document
from staff.models import Staff
from tools.models import ToolEquipment


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            # messages.error(request, 'Invalid username or password')
            messages.error(request, 'Invalid username or password', extra_tags='login_error')
    return render(request, 'login.html')

# def custom_permission_denied_view(request, exception=None):
#     return render(request, '404.html', status=404)

@login_required
def dashboard(request):
    if request.user.is_superuser:
        # clients = Client.objects.annotate(staff_count=Count('staff'))
        # total_clients = clients.count()

        clients = Client.objects.all()
        users = User.objects.all()
        staff = Staff.objects.all()
        tools = ToolEquipment.objects.all()

        return render(
            request,
            'admin_dashboard.html',
            {
                'clients': clients,
                'users': users,
                'staff': staff,
                'tools': tools
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
    messages.success(request, 'You have been logged out successfully', extra_tags='logout_success')
    return redirect('login')


# Check if the user is an admin
def is_admin(user):
    return user.is_superuser

# @login_required
# @user_passes_test(is_admin)
# def create_client(request):
#     if request.method == 'POST':
#         form = ClientForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Client created successfully!')
#             return redirect('dashboard')
#         else:
#             messages.error(request, 'Error creating client. Please check the form and try again.')
#     else:
#         form = ClientForm()

#     return render(request, 'create_client.html', {'form': form})

# @login_required
# @user_passes_test(is_admin)
# def client_list(request):
#     clients = Client.objects.all()
#     return render(request, 'client_list.html', {'clients': clients})

# @login_required
# @user_passes_test(is_admin)
# def create_user(request):
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.username = form.cleaned_data['username']  # Set the username
#             user.set_password(form.cleaned_data['password'])  # Set the password securely
#             user.save()
#             # messages.success(request, f"User {user.first_name} {user.last_name} created successfully!")
#             messages.success(request, f"User {user.first_name} {user.last_name} created successfully!", extra_tags='user_creation')
#             return redirect('dashboard')
#         else:
#             messages.error(request, "Error creating user. Please check the form and try again.", extra_tags='user_creation_error')
#             # messages.error(request, "Error creating user. Please check the form and try again.")

#     else:
#         form = UserForm()

#     return render(request, 'create_user.html', {'form': form})

# @login_required
# def client_detail(request, client_id):
#     if request.user.client_id == client_id or request.user.is_superuser:
#         client = get_object_or_404(Client, id=client_id)
#         users = client.user_set.all()  # Retrieve associated users
#         # jobs = client.jobs.all().select_related('staff')  # Retrieve associated jobs with staff
#         # if len(jobs) < 1:
#         staff_members = Staff.objects.filter(client_id=client_id).all()
#         # else:
#         #     staff_members = {job.staff for job in jobs}  # Get unique staff members from jobs
#         tools_equipment = client.tools_equipment.all()  # Retrieve tools and equipment
#         documents = Document.objects.filter(client=client)
#         document_status = {category.name: None for category in DocumentCategory}

#         for doc in documents:
#             document_status[doc.category] = doc

#         return render(
#             request,
#             'client_detail.html',
#             {
#                 'client': client,
#                 'users': users,
#                 'staff_members': staff_members,
#                 'tools_equipment': tools_equipment,
#                 'document_status': document_status,
#             }
#         )
#     else:
#         return render(request, '404.html')

# @login_required
# def update_user(request):
#     user = request.user
#     if request.method == 'POST':
#         form = UserUpdateForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Your profile has been updated successfully!")
#             return redirect('dashboard')
#         else:
#             messages.error(request, "Please correct the errors below.")
#     else:
#         form = UserUpdateForm(instance=user)

#     return render(request, 'update_user.html', {'form': form})

# @login_required
# @user_passes_test(is_admin)
# def user_list(request):
#     users = User.objects.select_related('client').all()  # Assuming User has a foreign key to Client
#     return render(request, 'user_list.html', {'users': users})

# @login_required
# @user_passes_test(is_admin)
# def edit_or_delete_user(request, user_id):
#     user = get_object_or_404(User, id=user_id)
#     if request.method == 'POST':
#         if 'update' in request.POST:  # Handle update
#             form = UserUpdateForm(request.POST, instance=user)
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, "User updated successfully!")
#                 return redirect('user_list')
#             else:
#                 messages.error(request, "Error updating user. Please correct the form.")
#         elif 'delete' in request.POST:  # Handle delete
#             user.delete()
#             messages.success(request, "User deleted successfully!")
#             return redirect('user_list')
#     else:
#         form = UserUpdateForm(instance=user)

#     return render(request, 'edit_or_delete_user.html', {'form': form, 'user': user})

# def user_denied(request):
#     return render(request, '404.html')