from django.http import JsonResponse
from django.views.generic.base import View
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from goods.models import SPU, Brand, GoodsCategory
from meiduo_admin.serializers.spu import SpuSerializer
from meiduo_admin.utils import PageNum


class SPUView(ModelViewSet):
	serializer_class = SpuSerializer
	pagination_class = PageNum
	queryset = SPU.objects.all()

	def showbrands(self,request):

		brands = Brand.objects.all()
		datalist = []
		for brand in brands:
			datalist.append({"id": brand.id,"name": brand.name})
		return Response(datalist)

	def showcategories(self,request):
		categories = GoodsCategory.objects.all()
		datalist = []
		for category in categories:
			datalist.append({"id": category.id,"name": category.name})
		return Response(datalist)

	def showsubcategories(self,request,pk):
		categories = GoodsCategory.objects.filter(parent_id=pk)
		datalist = []
		for category in categories:
			datalist.append({"id": category.id,"name": category.name})
		datadict = {'subs': datalist}
		return Response(datadict)

class SPUTestView(View):

	def get(self,request):
		return JsonResponse({"goods test":'ok'})