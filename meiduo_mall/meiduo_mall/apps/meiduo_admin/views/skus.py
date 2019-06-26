from rest_framework.viewsets import ModelViewSet

from goods.models import SKU
from meiduo_admin.serializers.skus import SKUSerializer
from meiduo_admin.utils import PageNum


class SkusView(ModelViewSet):

	pagination_class = PageNum
	serializer_class = SKUSerializer
	queryset = SKU.objects.all()