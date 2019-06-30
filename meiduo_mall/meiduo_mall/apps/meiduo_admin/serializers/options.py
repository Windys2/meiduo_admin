from rest_framework import serializers

from goods.models import SpecificationOption


class OptionsSerializer(serializers.ModelSerializer):

	spec = serializers.StringRelatedField()
	spec_id = serializers.IntegerField()

	class Meta:

		model = SpecificationOption
		fields = '__all__'
