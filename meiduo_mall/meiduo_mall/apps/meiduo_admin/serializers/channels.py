from rest_framework import serializers

from goods.models import GoodsChannel


class ChannelSerialiser(serializers.ModelSerializer):
	category = serializers.StringRelatedField()
	category_id = serializers.IntegerField()
	group = serializers.StringRelatedField()
	group_id = serializers.IntegerField()

	class Meta:

		model = GoodsChannel
		fields = '__all__'