from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from goods.models import GoodsVisitCount


class GoodsVisitSerializer(ModelSerializer):

	category = serializers.StringRelatedField()

	class Meta:
		model = GoodsVisitCount
		fields = ["category",'count']
