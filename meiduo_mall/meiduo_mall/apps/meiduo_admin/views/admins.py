from django.contrib.auth.models import Group
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from meiduo_admin.serializers.groups import GroupSerializer
from meiduo_admin.serializers.user import UserSerializer
from meiduo_admin.utils import PageNum
from users.models import User


class AdminView(ModelViewSet):

	queryset = User.objects.filter(is_staff=True)
	serializer_class = UserSerializer
	pagination_class = PageNum

	def show_groups(self,request):

		groups = Group.objects.all()
		ser = GroupSerializer(groups,many=True)
		return Response(ser.data)


