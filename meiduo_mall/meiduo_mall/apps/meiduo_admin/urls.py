from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from .views import increment,users,skus
# from django import views

urlpatterns = [
	# url(r'^skus/$', skus.SkusView.as_view()),
	url(r'^users/$', users.UserView.as_view()),

	url(r'^statistical/goods_day_views/$', increment.GoodsVisitView.as_view()),

	url(r'^statistical/month_increment/$', increment.UserMonthCountView.as_view()),

	url(r'^statistical/day_orders/$', increment.UserDayOrdersView.as_view()),

	url(r'^statistical/day_active/$', increment.UserDayActiveView.as_view()),

	url(r'^statistical/day_increment/$', increment.UserDayCountView.as_view()),

	url(r'^authorizations/$', obtain_jwt_token),
	url(r'^statistical/total_count/$', increment.UserTotalcountView.as_view()),
	]

router = DefaultRouter()
router.register('skus',skus.SkusView,base_name='skus')
urlpatterns += router.urls
