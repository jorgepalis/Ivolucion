from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Role


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ('email', 'name', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)

        client_role = Role.objects.filter(name__iexact='client').first()
        if client_role and getattr(user, 'role_id', None) is None:
            setattr(user, 'role', client_role)
            user.save(update_fields=['role'])

        return user


class RegisterResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'role_name']
    
    role_name = serializers.CharField(source='role.name', read_only=True)