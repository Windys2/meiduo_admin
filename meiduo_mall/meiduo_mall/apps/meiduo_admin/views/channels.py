from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from goods.models import GoodsChannel, GoodsChannelGroup, GoodsCategory
from meiduo_admin.serializers.channels import ChannelSerialiser
from meiduo_admin.utils import PageNum


class ChannelView(ModelViewSet):

	pagination_class = PageNum
	serializer_class = ChannelSerialiser
	queryset = GoodsChannel.objects.all()

	def showchannel_types(self,request):

		channel_types = GoodsChannelGroup.objects.all()
		datalist = []
		for _ in channel_types:

			datalist.append({
				'id':_.id,
				"name":_.name
			})

		return Response(datalist)

	def	showcategories(self,request):

		categories = GoodsCategory.objects.filter(parent=None)
		datalist = []
		for _ in categories:
			datalist.append({
				'id': _.id,
				"name": _.name
			})

		return Response(datalist)
