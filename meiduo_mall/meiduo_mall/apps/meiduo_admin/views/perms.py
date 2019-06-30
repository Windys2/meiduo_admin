from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from meiduo_admin.serializers.perms import PermsSerializer
from meiduo_admin.utils import PageNum


class PermsView(ModelViewSet):

	pagination_class = PageNum
	serializer_class = PermsSerializer
	queryset = Permission.objects.all()

	def show_content(self,request):

		contents = ContentType.objects.all()
		datalist = []
		for content in contents:
			datalist.append({'id':content.id})
		return Response(datalist)