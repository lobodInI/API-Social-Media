from typing import Type

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from social_media.models import Post, Comment, Like
from social_media.permissions import IsAuthorOrReadOnly
from social_media.serializers import (
    LikeSerializer,
    CommentSerializer,
    CommentListSerializer,
    CommentDetailSerializer,
    PostSerializer,
    PostListSerializer,
    PostDetailSerializer,
    PostImageSerializer,
)


class PostPagination(PageNumberPagination):
    page_size = 5
    max_page_size = 50


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("author")
    serializer_class = PostSerializer
    pagination_class = PostPagination
    permission_classes = (IsAuthorOrReadOnly,)

    filter_backends = [filters.SearchFilter]
    search_fields = ["hashtag"]

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "list":
            return PostListSerializer
        if self.action == "retrieve":
            return PostDetailSerializer
        if self.action == "like":
            return LikeSerializer
        if self.action == "upload_image":
            return PostImageSerializer
        return self.serializer_class

    @action(
        detail=True,
        methods=["POST"],
        permission_classes=[IsAuthenticated],
        url_path="like",
    )
    def like(self, request, pk) -> Response:
        post = get_object_or_404(
            Post,
            id=pk,
        )
        author = request.user
        serializer = LikeSerializer(
            data={"post": post.id, "author": author.id}
        )
        serializer.is_valid(
            raise_exception=True,
        )
        serializer.save()
        response_serializer = PostDetailSerializer(post)
        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=["POST"],
        permission_classes=[IsAuthenticated],
        url_path="unlike",
    )
    def unlike(self, request, pk):
        post = get_object_or_404(
            Post,
            id=pk,
        )
        author = request.user
        user_like = Like.objects.filter(
            post__id=post.id,
            author__id=author.id,
        )
        if not user_like:
            raise ValidationError("You can't do this")
        user_like.delete()
        serializer = PostDetailSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["POST"],
        permission_classes=[IsAuthenticated],
        url_path="upload_image",
    )
    def upload_image(self, request, pk=None):
        comment = self.get_object()
        serializer = self.get_serializer(comment, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer) -> None:
        serializer.save(author=self.request.user)


class CommentPagination(PageNumberPagination):
    page_size = 5
    max_page_size = 50


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related("post")
    serializer_class = CommentSerializer
    pagination_class = PostPagination
    permission_classes = (IsAuthorOrReadOnly,)

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "list":
            return CommentListSerializer
        if self.action == "retrieve":
            return CommentDetailSerializer
        return self.serializer_class

    def perform_create(self, serializer) -> None:
        serializer.save(author=self.request.user)
