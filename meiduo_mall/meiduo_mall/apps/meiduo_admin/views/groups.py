from django.contrib.auth.models import Group, Permission
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from meiduo_admin.serializers.groups import GroupSerializer
from meiduo_admin.serializers.perms import PermsSerializer
from meiduo_admin.utils import PageNum


class GroupView(ModelViewSet):
	queryset = Group.objects.all()
	serializer_class = GroupSerializer
	pagination_class = PageNum

	def show_perms(self,request):

		perms = Permission.objects.all()
		ser = PermsSerializer(perms,many=True)
		return Response(ser.data)