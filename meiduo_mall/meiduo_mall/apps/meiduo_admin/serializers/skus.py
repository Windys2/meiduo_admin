from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.utils import model_meta

from goods.models import SKU, SKUSpecification, SPUSpecification, SpecificationOption


class SpecSerializer(ModelSerializer):

	class Meta:
		model = SKUSpecification
		fields = ('spec_id',"option_id")


class SKUSerializer(ModelSerializer):

	category = serializers.StringRelatedField()
	spu = serializers.StringRelatedField()
	category_id = serializers.IntegerField()
	spu_id = serializers.IntegerField()
	specs = SpecSerializer(many = True,read_only=True)

	class Meta:
		model = SKU
		fields = "__all__"

	def create(self,validated_data):

		specs = self.context.get('request').data.get('specs')

		sku = SKU.objects.create(**validated_data)

		for spec in specs:

			SKUSpecification.objects.create(sku=sku,spec_id = spec['spec_id'],option_id=spec['option_id'])

		return sku

	def update(self, instance, validated_data):
		specs = self.context.get('request').data.get('specs')

		for spec in specs:
			print(spec)
			SKUSpecification.objects.filter(sku_id=instance.id,spec_id=spec['spec_id']).update(option_id=spec['option_id'])
			# SKUSpecification.objects.create(sku=instance, spec_id=spec['spec_id'], option_id=spec['option_id'])

		info = model_meta.get_field_info(instance)
		del validated_data['specs']
		for attr, value in validated_data.items():
			if attr in info.relations and info.relations[attr].to_many:
				field = getattr(instance, attr)
				field.set(value)
			else:
				setattr(instance, attr, value)
		instance.save()


		return instance


class OptionsSerializer(ModelSerializer):

	class Meta:
		model = SpecificationOption
		fields = "__all__"

class SpecsSerializer(ModelSerializer):

	spu = serializers.StringRelatedField()
	spu_id = serializers.IntegerField()
	options = OptionsSerializer(many=True)

	class Meta:
		model= SPUSpecification
		fields = "__all__"