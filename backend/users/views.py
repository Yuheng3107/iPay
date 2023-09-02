from rest_framework import status
from rest_framework.views import APIView, Response
from django.contrib.auth import get_user_model, login, logout
from django.http import HttpResponse
from django.middleware.csrf import get_token
from .serializer import UserSerializer
from random_username.generate import generate_username

# Create your views here.
class UserCreateView(APIView):
    def post(self, request):
        """API used internally to create users in DB from social logins"""
        # Need to serialize data
        fields = ["first_name", "last_name", "email"]
        # Ensures all fields are there
        for field in fields:
            if field not in request.data:
                return Response(f"Please input data into {field}", status=status.HTTP_400_BAD_REQUEST)
        fields = {field: request.data[field] for field in fields}
        User = get_user_model()
        response = HttpResponse()
        csrf_token = get_token(request)
        try:
            # check whether email is registered already
            user = User.objects.get(email=fields["email"])
            login(request, user)
            response.write("User already in database")
            return response
        except User.DoesNotExist:
            username = generate_username(1)[0]
            user = User.objects.create_user(**fields, username=username)
            user.save()
            login(request, user)
            response.write("User Successfully Registered")
        return response