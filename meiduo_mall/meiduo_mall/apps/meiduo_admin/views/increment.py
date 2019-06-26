from datetime import date, timedelta

from django.shortcuts import render
from rest_framework.mixins import RetrieveModelMixin

# Create your views here.
from rest_framework.generics import ListAPIView, GenericAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from goods.models import GoodsVisitCount
from meiduo_admin.serializers.increment import GoodsVisitSerializer
from orders.models import OrderInfo
from users.models import User


class UserTotalcountView(APIView):
	permission_classes = [IsAdminUser]
	
	def get(self,request):
		
		count = User.objects.all().count()
		now_date = date.today()
		
		return Response({"count":count,"date":now_date})
		


class UserDayCountView(APIView):
	permission_classes = [IsAdminUser]
 

	def get(self, request):
		now_date = date.today()
		count = User.objects.filter(date_joined__gte=now_date).count()

		return Response({"count": count, "date": now_date})


class UserDayActiveView(APIView):
	permission_classes = [IsAdminUser]

	def get(self, request):
		now_date = date.today()
		
		count = User.objects.filter(last_login__gte=now_date).count()

		return Response({"count": count, "date": now_date})


class UserDayOrdersView(APIView):

	permission_classes = [IsAdminUser]

	def get(self, request):

		now_date = date.today()

		count = User.objects.filter(orders__create_time__gte=now_date).values("pk").distinct().count()
		# count = OrderInfo.objects.filter
		return Response({"count": count, "date": now_date})


class UserMonthCountView(APIView):

	permission_classes = [IsAdminUser]

	def get(self, request):

		now_date = date.today()
		first_date = now_date - timedelta(29)
		data = []
		for i in range(30):
			start_date = first_date + timedelta(i)
			next_date = start_date + timedelta(1)
			count = User.objects.filter(date_joined__gte=now_date,date_joined__lt=next_date).count()
			data.append({"count": count, "date": start_date})
		return Response(data)


class GoodsVisitView(ListAPIView):
	permission_classes = [IsAdminUser]
	now_date = date.today()
	queryset = GoodsVisitCount.objects.filter(date__gte=now_date)
	serializer_class = GoodsVisitSerializer

