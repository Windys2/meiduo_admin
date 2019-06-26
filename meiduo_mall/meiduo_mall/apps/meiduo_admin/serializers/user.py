from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):

	password = serializers.CharField(write_only=True,min_length=8,max_length=20)
	username = serializers.CharField(min_length=5,max_length=20)

	class Meta:
		model = User
		fields = ["id",'username','mobile','email','password']

	def create(self, validated_data):

		user = User.objects.create_user(**validated_data)

		return user

