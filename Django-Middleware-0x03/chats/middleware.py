import logging
from datetime import datetime, time
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.http import HttpResponseForbidden
logger = logging.getLogger('request_logger')

class RequestLoggingMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        self.get_response = get_response
        handler = logging.FileHandler('requests.log')
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        self.jwt_authenticator = JWTAuthentication()

    def __call__(self, request):
        user = 'Anonymous'
        try:
            # Try to authenticate user via JWT token manually
            user_auth_tuple = self.jwt_authenticator.authenticate(request)
            if user_auth_tuple:
                user, _ = user_auth_tuple
        except AuthenticationFailed:
            pass

        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Define allowed access time window (6 AM to 9 PM)
        self.start_time = time(6, 0, 0)   # 6:00:00 AM
        self.end_time = time(21, 0, 0)    # 9:00:00 PM (21:00)

    def __call__(self, request):
        current_time = datetime.now().time()

        # Check if current time is outside allowed range
        # Allowed: 06:00 <= current_time <= 21:00
        if not (self.start_time <= current_time <= self.end_time):
            # Optionally, restrict only chat-related paths here:
            # if request.path.startswith('/chat/') or whatever your chat URL prefix is
            # For now, restrict all requests outside time window:
            return HttpResponseForbidden("Chat access is allowed only between 6 AM and 9 PM.")

        response = self.get_response(request)
        return response