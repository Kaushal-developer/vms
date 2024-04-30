from django.contrib.auth import logout
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.shortcuts import render
from lib.renderer import CustomJSONRenderer
from lib.views import BaseAPIView
from django.contrib.auth import authenticate


class LoginView(ObtainAuthToken):
    renderer_classes = [CustomJSONRenderer]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if not user:
            raise ValidationError({"non_field_errors": [f"User is not active."]})
        token, created = Token.objects.get_or_create(user=user)
        # Store token in both cookie and session storage
        request.session['auth_token'] = token.key
        data = {"token": token.key}
        return Response(data=data, status=status.HTTP_200_OK)


class LogoutView(BaseAPIView):

    def post(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response(data={"message": "Logged Out Successfully"}, status=status.HTTP_200_OK)
