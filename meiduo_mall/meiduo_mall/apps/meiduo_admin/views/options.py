from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from goods.models import SpecificationOption, SPUSpecification
from meiduo_admin.serializers.options import OptionsSerializer
from meiduo_admin.utils import PageNum


class OptionsView(ModelViewSet):

	serializer_class = OptionsSerializer
	pagination_class = PageNum
	queryset = SpecificationOption.objects.all()

	def showspecs(self,request):

		specs = SPUSpecification.objects.all()
		datalist = []
		for spec in specs:
			datalist.append({
				"id": spec.id,
				"name": spec.name
			})
		return Response(datalist)
