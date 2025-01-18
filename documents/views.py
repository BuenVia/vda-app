from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from .forms import DocumentUploadForm
from .models import Client, Document
from .enums import DocumentCategory



# Create your views here.
@login_required
# @user_passes_test(is_admin)
def document_list(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    documents = Document.objects.filter(client=client)
    document_status = {category.name: None for category in DocumentCategory}
    
    for doc in documents:
        document_status[doc.category] = doc
    
    return render(request, 'documents/document_list.html', {'client': client, 'document_status': document_status})

@login_required
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

    return render(request, 'documents/upload_document.html', {'form': form, 'client': client, 'category': category})

@login_required
# @user_passes_test(lambda u: u.is_superuser)
def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    client_id = document.client.id  # Save client ID for redirecting
    document.delete()  # Delete the document
    messages.success(request, "Document deleted successfully!")
    return redirect('client_detail', client_id=client_id)

