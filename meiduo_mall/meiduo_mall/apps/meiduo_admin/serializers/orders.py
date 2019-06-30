from rest_framework import serializers

from goods.models import SKU
from meiduo_admin.serializers.skus import SKUSerializer
from orders.models import OrderInfo, OrderGoods


class SKUsSerializer(serializers.ModelSerializer):

	sku = SKUSerializer()

	class Meta:
		model = OrderGoods
		fields = ('count','price','sku')

class OrdersSerializer(serializers.ModelSerializer):

	skus = SKUsSerializer(many=True)

	class Meta:

		model = OrderInfo
		fields ='__all__'