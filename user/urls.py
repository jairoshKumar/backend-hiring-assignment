# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ClientViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'clients', ClientViewSet)

urlpatterns = [
    path('rest/', include(router.urls)),
#     path('signup/', UserRegistrationAPIView.as_view(), name='signup'),
#     path("login/", LoginView.as_view()),
#     path("logout/", LogoutView.as_view()),
]
