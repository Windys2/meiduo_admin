from django.conf import settings
from django.db.models import Model
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
import os
from goods.models import Brand
from meiduo_admin.serializers.brands import BrandSerializer
from meiduo_admin.utils import PageNum
from fdfs_client.client import Fdfs_client
from django.db import models

class BrandsView(ModelViewSet):
	pagination_class = PageNum
	serializer_class = BrandSerializer
	queryset = Brand.objects.all()

	def create(self,request):

		data = request.FILES.get('logo')
		fdfs_config_path = os.path.join(settings.BASE_DIR,'utils/fdfs/client.conf')
		client = Fdfs_client(fdfs_config_path)
		ret = client.upload_by_buffer(data.read())
		print(ret)
		if ret['Status'] != 'Upload successed.':
			return Response({'errmsg': 'upload failed'}, code = 400)
		else:
			img_address = ret.get('Remote file_id')
			first_letter = request.data.get('first_letter')
			name= request.data.get('name')
			brand = Brand.objects.create(first_letter=first_letter,name=name,logo=img_address)
			ser = self.get_serializer(brand)
			return Response(ser.data)

	def update(self,request,pk):

		data = request.FILES.get('logo')
		fdfs_config_path = os.path.join(settings.BASE_DIR,'utils/fdfs/client.conf')
		client = Fdfs_client(fdfs_config_path)
		ret = client.upload_by_buffer(data.read())
		# print(ret)
		if ret['Status'] != 'Upload successed.':
			return Response({'errmsg': 'upload failed'}, code = 400)
		else:
			img_address = ret.get('Remote file_id')
			first_letter = request.data.get('first_letter')
			name= request.data.get('name')
			brand = self.get_object()
			brand.first_letter=first_letter
			brand.name=name
			brand.logo = img_address
			brand.save()
			ser = self.get_serializer(brand)
			return Response(ser.data)




'''
mysql -h127.0.0.1 -uroot -pmysql meiduo_tbd39 < goods_data.sql
{
    'Storage IP': '192.168.47.128',
    'Group name': 'group1',
    'Uploaded size': '8.00KB',
    'Status': 'Upload successed.',
    'Local file name': '/home/python/Desktop/1.jpg',
    'Remote file_id': 'group1/M00/00/00/wKgvgFyVsQKANIKnAAAhg8MeEWU833.jpg'
}

'''