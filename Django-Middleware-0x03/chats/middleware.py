import logging
from datetime import datetime, time as dt_time
import time
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.http import HttpResponseForbidden
from django.http import JsonResponse



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
     
        self.start_time = dt_time(6, 0, 0)  
        self.end_time = dt_time(21, 0, 0)   

    def __call__(self, request):
        current_time = datetime.now().time()

     
        if not (self.start_time <= current_time <= self.end_time):
           
            return HttpResponseForbidden("Chat access is allowed only between 6 AM and 9 PM.")

        response = self.get_response(request)
        return response

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
       
        self.ip_message_times = {}

    def __call__(self, request):
    
        if request.method == "POST":
            ip = self.get_client_ip(request)
            now = time.time()
            window = 60  
            limit = 5   
            
          
            timestamps = self.ip_message_times.get(ip, [])
            
       
            timestamps = [t for t in timestamps if now - t < window]
            
            if len(timestamps) >= limit:
             
                return JsonResponse({"error": "Too many messages sent. Please wait before sending more."}, status=429)
            
            
            timestamps.append(now)
            self.ip_message_times[ip] = timestamps
        
      
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
     
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)

    
        if not user or not user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)

      
        user_role = getattr(user, 'role', '').lower()

        if user_role not in ['admin', 'moderator']:
            return JsonResponse({"error": "You do not have permission to perform this action"}, status=403)

    
        response = self.get_response(request)
        return response