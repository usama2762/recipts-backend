from rest_framework import serializers
from .models import Image, Mall
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    """
    Serializer for User Operations.
    """

    class Meta:
        model = User
        fields = ['id', 'username',  'email', 'first_name', 'last_name',]
        extra_kwargs = {"password": {"write_only": True},
                        "is_staff": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user_obj = User(**validated_data)
        user_obj.set_password(password)
        user_obj.save()
        return user_obj

    def update(self, instance, validated_data):
        instance.email = validated_data.pop('email', instance.email)
        instance.first_name = validated_data.pop('first_name', instance.first_name)
        instance.last_name = validated_data.pop('last_name', instance.last_name)
        instance.save()
        return instance


class ImageSerializer(serializers.ModelSerializer):

    """
    Serializer for Image Endpoints
    """

    class Meta:
        model = Image
        fields = '__all__'


class MallDetailSerializer(serializers.ModelSerializer):

    """
    Serializer for Mall Depth Serialization
    """
    attachedImages = ImageSerializer(many=True)

    class Meta:
        model = Mall
        fields = '__all__'


class MallSerializer(serializers.ModelSerializer):

    """
    Serializer for Mall Endpoints
    """
    attachedImages = serializers.ListField(allow_null=True)
    class Meta:
        model = Mall
        fields = '__all__'
        deoth = 1

    def create(self, validated_data):
        attachedImages = validated_data.pop('attachedImages', [])
        mall_obj = Mall(**validated_data)
        mall_obj.save()
        mall_obj.attachedImages.add(*attachedImages[0])
        return mall_obj

    def update(self, instance, validated_data):
        # instance.user = validated_data.pop('user', instance.user)
        instance.save()
        return instance

    def to_representation(self, instance):
        return MallDetailSerializer(instance).data