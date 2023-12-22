from rest_framework import serializers

from social_media.models import Post, Comment, Like


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ("id", "author", "post")

    def validate(self, data):
        user_like = Like.objects.filter(
            post_id=data["post"], author_id=data["author"]
        )
        if user_like:
            raise serializers.ValidationError(
                "Your like has already been taken"
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "post",
            "content",
            "author",
            "created_at",
        )


class CommentListSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="nickname", many=False, read_only=True
    )
    post = serializers.SlugRelatedField(
        slug_field="title", many=False, read_only=True
    )

    class Meta:
        model = Comment
        fields = (
            "id",
            "post",
            "content",
            "author",
            "created_at",
        )


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "created_at",
            "hashtag",
            "content",
            "image",
        )


class CommentDetailSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="nickname", many=False, read_only=True
    )
    post = PostSerializer(many=False, read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "post",
            "content",
            "author",
            "created_at",
        )


class PostListSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="nickname"
    )
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    def get_comments_count(self, instance) -> int:
        return instance.comments.count()

    def get_likes_count(self, instance) -> int:
        return instance.likes.count()

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "created_at",
            "title",
            "image",
            "hashtag",
            "comments_count",
            "likes_count",
        )


class PostCommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="nickname", many=False, read_only=True
    )

    class Meta:
        model = Comment
        fields = (
            "id",
            "author",
            "created_at",
            "content",
        )


class PostLikeSerializer(LikeSerializer):
    author = serializers.SlugRelatedField(
        slug_field="nickname", many=False, read_only=True
    )

    class Meta:
        model = Like
        fields = ("id", "author")


class PostDetailSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="nickname", many=False, read_only=True
    )
    likes = PostLikeSerializer(many=True, read_only=True)
    comments = PostCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "created_at",
            "title",
            "content",
            "image",
            "hashtag",
            "comments",
            "likes",
        )


class PostImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(read_only=False)

    class Meta:
        model = Post
        fields = ("id", "image")
