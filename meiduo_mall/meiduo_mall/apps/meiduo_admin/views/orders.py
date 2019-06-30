from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from meiduo_admin.serializers.orders import OrdersSerializer
from meiduo_admin.utils import PageNum
from orders.models import OrderInfo


class OrdersView(ReadOnlyModelViewSet):

	queryset = OrderInfo.objects.all()
	pagination_class = PageNum
	serializer_class = OrdersSerializer

	@action(methods=['put'],detail=True)
	def status(self,request,pk):

		order = self.get_object()
		order.status = request.data['status']
		order.save()
		ser = self.get_serializer(order)
		return Response(ser.data)
