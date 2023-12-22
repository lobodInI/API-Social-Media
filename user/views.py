from django.db.models import Count
from django.http import Http404
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenBlacklistView

from user.models import User, UserFollowing
from user.serializers import (
    UserSerializer,
    UserListSerializer,
    UserDetailSerializer,
    UserFollowingSerializer,
)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter]
    search_fields = ["nickname", "city"]

    def get_queryset(self):
        queryset = self.queryset.annotate(
            count_following=Count("following"),
            count_followers=Count("followers"),
        )

        return queryset

    def get_object(self):
        return self.request.user


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserDeleteView(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserFollowingView(viewsets.ModelViewSet):
    queryset = UserFollowing.objects.all()
    serializer_class = UserFollowingSerializer
    permission_classes = [IsAuthenticated]


class UserFollow(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def post(self, request, pk):
        user = request.user
        follower = self.get_object(pk)
        if user != follower:
            UserFollowing.objects.create(
                user_id=user,
                user_following=follower
            )
            serializer = UserDetailSerializer(follower)
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = request.user
        follower = self.get_object(pk)
        following = UserFollowing.objects.filter(
            user_id=user,
            user_following=follower
        ).first()
        following.delete()
        serializer = UserDetailSerializer(follower)
        return Response(serializer.data)


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class LogoutUserView(TokenBlacklistView):
    """Access token expiry as short as possible"""

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            return Response({"detail": "Logged out successfully"}, status=200)
        return response
