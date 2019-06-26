from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from goods.models import SKU, SKUSpecification


class SpecSerializer(ModelSerializer):

	class Meta:
		model = SKUSpecification
		fields = ('spec_id',"option_id")


class SKUSerializer(ModelSerializer):

	category = serializers.StringRelatedField()
	spu = serializers.StringRelatedField()
	category_id = serializers.IntegerField()
	spu_id = serializers.IntegerField()
	specs = SpecSerializer(many = True)

	class Meta:
		model = SKU
		fields = "__all__"