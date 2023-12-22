from django.urls import path
from rest_framework_simplejwt.views import (
    TokenVerifyView,
    TokenRefreshView,
    TokenObtainPairView,
)

from user.views import (
    UserListView,
    UserDetailView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
    UserFollow,
    ManageUserView,
    LogoutUserView,
)

urlpatterns = [
    path("", UserListView.as_view(), name="user-list"),
    path("me/", ManageUserView.as_view(), name="manage"),
    path("<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("register/", UserCreateView.as_view(), name="user-register"),
    path("<int:pk>/update/", UserUpdateView.as_view(), name="user-update"),
    path("<int:pk>/delete/", UserDeleteView.as_view(), name="user-delete"),
    path("follow/<int:pk>/", UserFollow.as_view(), name="user-follow"),
    path("logout/", LogoutUserView.as_view(), name="logout"),
    path("token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token-verify"),
]
app_name = "user"
