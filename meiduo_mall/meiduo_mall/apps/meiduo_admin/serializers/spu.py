from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from goods.models import SPU


class SpuSerializer(ModelSerializer):

	brand = serializers.StringRelatedField()
	brand_id = serializers.IntegerField()
	category1_id = serializers.IntegerField()
	category2_id = serializers.IntegerField()
	category3_id = serializers.IntegerField()

	class Meta:

		model = SPU
		exclude = ('category1','category2','category3')

