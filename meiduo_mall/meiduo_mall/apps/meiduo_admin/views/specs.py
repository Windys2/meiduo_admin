from django.http import JsonResponse
from django.views.generic.base import View
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet

from goods.models import SPUSpecification
from meiduo_admin.serializers.specs import SpecsSerializer
from meiduo_admin.utils import PageNum


class SpecView(ModelViewSet):

	serializer_class = SpecsSerializer
	pagination_class = PageNum
	queryset = SPUSpecification.objects.all()

	# @action(methods = ['get'],detail = False)
	# def simple(self,request):
	#
	# 	ser = SpecsSerializer(self.queryset, many= True)
	# 	# return Response(ser.data)
	# 	pag = self.pagination_class()
	# 	pag.page = pag.paginate_queryset(self.queryset,request)
	#
	# 	return pag.get_paginated_response(ser.data)


class SpecTestView(View):

	def get(self, request):
		return JsonResponse({"specs test": 'ok'})
