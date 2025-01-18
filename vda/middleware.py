from datetime import timedelta
from django.utils.timezone import now
from django.conf import settings

class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Get the last activity time from the session
            last_activity = request.session.get('last_activity')

            # If there is a last activity time
            if last_activity:
                last_activity_time = now() - timedelta(seconds=settings.SESSION_COOKIE_AGE)

                # Log out if the last activity exceeds the session timeout
                if last_activity < last_activity_time.timestamp():
                    from django.contrib.auth import logout
                    logout(request)
                    request.session.flush()  # Clear the session data
            # Update the last activity time in the session
            request.session['last_activity'] = now().timestamp()

        response = self.get_response(request)
        return response
