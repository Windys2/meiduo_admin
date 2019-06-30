from django.contrib.auth.models import Permission
from rest_framework import serializers


class PermsSerializer(serializers.ModelSerializer):

	class Meta:

		model = Permission
		fields = ('id','name','codename')