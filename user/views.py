# views.py
from rest_framework import viewsets
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.authentication import TokenAuthentication
from .serializers import UserSerializer
from rest_framework import status
from rest_framework import filters as rest_framework_filters
from django_filters import rest_framework as filters

class UserFilter(filters.FilterSet):

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "mobile",
            "email",
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication,]
    ordering = ["updated_at"]
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_framework_filters.OrderingFilter,
        rest_framework_filters.SearchFilter,
    ]
    filterset_class = UserFilter
    search_fields = ["id", "first_name", "last_name", "mobile", "email"]

    def create(self, request, *args, **kwargs):
        user_data = request.data.copy()

        user_data["email"] = request.data.get("username")
        password = request.data.get("password", None)

        # Check if a password is provided in the request
        if password:
            # Create the user instance without saving to the database yet
            user_instance = User(**user_data)

            # Use set_password to securely set the user's password
            user_instance.set_password(password)

            # Save the user instance with the hashed password
            user_instance.save()

            # Continue with the default behavior for creating the user
            headers = self.get_success_headers(request.data)
            serializer = self.get_serializer(user_instance)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )

        else:
            # If no password is provided, you might want to handle this case accordingly
            return Response(
                {"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST
            )


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    authentication_classes = [TokenAuthentication,]
    ordering = ["updated_at"]
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_framework_filters.OrderingFilter,
        rest_framework_filters.SearchFilter,
    ]
    search_fields = ["id", "user__first_name", "user__last_name", "user__email", "user__username", "name"]