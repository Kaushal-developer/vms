
from django.shortcuts import HttpResponse

from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

class TokenAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Exclude certain URLs from token authentication
        exclude_urls = ['/generate_token/']
        if request.path in exclude_urls:
            return self.get_response(request)

        # Check if the user has a token in the request headers
        if 'Authorization' in request.headers:
            try:
                # Attempt to authenticate the user using TokenAuthentication
                user, _ = TokenAuthentication().authenticate(request)
                if user is not None:
                    request.user = user
                    return self.get_response(request)
            except (IndexError, AuthenticationFailed):
                pass  # Token is missing or invalid
        return HttpResponse('Invalid Token')
        
        
