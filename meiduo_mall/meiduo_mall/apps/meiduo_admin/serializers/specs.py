from rest_framework import serializers

from goods.models import SPUSpecification


class SpecsSerializer(serializers.ModelSerializer):

	spu_id = serializers.IntegerField()
	spu = serializers.StringRelatedField()
	class Meta:
		model = SPUSpecification
		fields = '__all__'