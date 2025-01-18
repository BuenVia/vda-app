from django.conf import settings

def version_context(request):
    return {"APP_VERSION": getattr(settings, "VERSION", "Unknown")}
