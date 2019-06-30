from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.utils import model_meta

from users.models import User


class UserSerializer(ModelSerializer):

	password = serializers.CharField(write_only=True,min_length=8,max_length=20)
	username = serializers.CharField(min_length=5,max_length=20)

	class Meta:
		model = User
		fields = ["id",'username','mobile','email','password']

	def create(self, validated_data):

		if self.context['request'].path=='/meiduo_admin/permission/admins/':
			print(self.context['request'].path)

			validated_data['is_staff']=True
			user = User.objects.create_user(**validated_data)
		else:
			user = User.objects.create_user(**validated_data)

		return user

	def update(self,instance,validated_data):
		password = validated_data['password']
		user = super().update(instance,validated_data)
		user.set_password(password)
		user.save()

		return user
