import os

from django.conf import settings
from fdfs_client.client import Fdfs_client
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from goods.models import SKUImage, SKU
from meiduo_admin.serializers.iamges import ImageSerializer
from meiduo_admin.utils import PageNum


class ImageView(ModelViewSet):

	serializer_class = ImageSerializer
	pagination_class = PageNum
	queryset = SKUImage.objects.all()

	def simple(self,request):

		skus = SKU.objects.all()
		datalist =[]
		for sku in skus:
			datalist.append({"id":sku.id,"name":sku.name})
		return Response(datalist)


	def create(self,request):

		data = request.FILES.get('image')
		fdfs_config_path = os.path.join(settings.BASE_DIR,'utils/fdfs/client.conf')
		client = Fdfs_client(fdfs_config_path)
		ret = client.upload_by_buffer(data.read())
		# print(ret)
		if ret['Status'] != 'Upload successed.':
			return Response({'errmsg': 'upload failed'}, code = 400)
		else:
			img_address = ret.get('Remote file_id')
			sku_id = request.data.get('sku')
			# name= request.data.get('name')
			image = SKUImage.objects.create(sku_id=sku_id,image=img_address)
			ser = self.get_serializer(image)
			return Response(ser.data,status=201)

	def update(self,request,pk):

		data = request.FILES.get('image')
		fdfs_config_path = os.path.join(settings.BASE_DIR,'utils/fdfs/client.conf')
		client = Fdfs_client(fdfs_config_path)
		ret = client.upload_by_buffer(data.read())
		# print(ret)
		if ret['Status'] != 'Upload successed.':
			return Response({'errmsg': 'upload failed'}, code = 400)
		else:
			img_address = ret.get('Remote file_id')
			sku_id = request.data.get('sku')
			image = SKUImage.objects.get(id=pk)
			image.sku_id=sku_id
			image.image=img_address
			image.save()
			ser = self.get_serializer(image)
			return Response(ser.data)