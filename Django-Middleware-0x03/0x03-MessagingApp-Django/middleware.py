import logging
from datetime import datetime
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

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
