from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from goods.models import SKU, GoodsCategory, SPU, SPUSpecification
from meiduo_admin.serializers.skus import SKUSerializer, SpecsSerializer
from meiduo_admin.utils import PageNum


class SkusView(ModelViewSet):

	pagination_class = PageNum
	serializer_class = SKUSerializer
	queryset = SKU.objects.all()

	def showcategories(self,request):

		categories = GoodsCategory.objects.filter(subs=None)
		datalist =[]
		for category in categories:
			datalist.append({"id":category.id,"name":category.name})
		return Response(datalist)

	def showspu(self,request):
		spus = SPU.objects.all()
		datalist =[]
		for spu in spus:
			datalist.append({"id":spu.id,"name":spu.name})
		return Response(datalist)

	def showspecs(self,request,pk):

		specs = SPUSpecification.objects.filter(spu_id = pk)
		ser = SpecsSerializer(specs,many=True)
		return Response(ser.data)
