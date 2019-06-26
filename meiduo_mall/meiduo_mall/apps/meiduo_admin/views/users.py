from rest_framework.generics import ListAPIView, ListCreateAPIView

from meiduo_admin.serializers.user import UserSerializer
from meiduo_admin.utils import PageNum
from users.models import User


class UserView(ListCreateAPIView):

	pagination_class = PageNum
	serializer_class = UserSerializer
	queryset = User.objects.all()

	def get_queryset(self):

		user_name = self.request.query_params.get('keyword')

		if not user_name:
			return self.queryset
		else:
			return User.objects.filter(username = user_name )

