from django.contrib.auth import get_user_model
from rest_framework import serializers

from user.models import UserFollowing


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "password",
            "nickname",
            "first_name",
            "last_name",
            "user_image",
            "city",
            "bio",
            "birthday",
            "date_registration",
            "is_staff",
        )
        read_only_fields = ("is_staff",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        if validated_data.get("user_image") is None:
            validated_data["user_image"] = instance.user_image
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user


class UserListSerializer(UserSerializer):
    count_following = serializers.IntegerField(read_only=True)
    count_followers = serializers.IntegerField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "password",
            "nickname",
            "first_name",
            "last_name",
            "user_image",
            "city",
            "bio",
            "birthday",
            "date_registration",
            "is_staff",
            "count_following",
            "count_followers",
        )
        read_only_fields = ("is_staff",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}


class UserDetailSerializer(UserSerializer):
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "nickname",
            "first_name",
            "last_name",
            "user_image",
            "city",
            "birthday",
            "bio",
            "date_registration",
            "is_staff",
            "following",
            "followers",
        )

    def get_following(self, obj):
        result = UserFollowingSerializer(obj.following.all(), many=True)
        return result.data

    def get_followers(self, obj):
        result = UserFollowersSerializer(obj.followers.all(), many=True)
        return result.data


class UserFollowingSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="user_following.id")
    nickname = serializers.ReadOnlyField(source="user_id.nickname")

    class Meta:
        model = UserFollowing
        fields = ("id", "nickname")


class UserFollowersSerializer(serializers.ModelSerializer):
    nickname = serializers.ReadOnlyField(source="user_id.nickname")

    class Meta:
        model = UserFollowing
        fields = ("user_id", "nickname")
