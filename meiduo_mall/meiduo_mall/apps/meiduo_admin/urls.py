from pprint import pprint

from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from meiduo_admin.views import goods, specs, options, channels, brands,images,orders,perms
from .views import increment,users,skus,groups,admins
# from django import views

urlpatterns = [
	url(r'^permission/groups/simple/$', admins.AdminView.as_view({'get': 'show_groups'})),
	url(r'^permission/simple/$', groups.GroupView.as_view({'get': 'show_perms'})),
	url(r'^permission/content_types/$', perms.PermsView.as_view({'get': 'show_content'})),

	url(r'^skus/simple/$', images.ImageView.as_view({'get': 'simple'})),
	url(r'^goods/channel_types/$', channels.ChannelView.as_view({'get': 'showchannel_types'})),
	url(r'^goods/categories/$', channels.ChannelView.as_view({'get': 'showcategories'})),

	url(r'^goods/specs/simple/$', options.OptionsView.as_view({'get': 'showspecs'})),
	# url(r'^goods/$', goods.SPUTestView.as_view()),
	# url(r'^goods/specs/$', specs.SpecTestView.as_view()),

	url(r'^goods/channel/categories/(?P<pk>\d+)/$', goods.SPUView.as_view({'get': 'showsubcategories'})),
	url(r'^goods/channel/categories/$', goods.SPUView.as_view({'get': 'showcategories'})),
	url(r'^goods/brands/simple/$', goods.SPUView.as_view({'get': 'showbrands'})),
	url(r'^goods/(?P<pk>\d+)/specs/$', skus.SkusView.as_view({'get': 'showspecs'})),
	url(r'^goods/simple/$', skus.SkusView.as_view({'get':'showspu'})),
	url(r'^skus/categories/$', skus.SkusView.as_view({'get':'showcategories'})),
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
router.register('permission/admins',admins.AdminView,base_name='admins')
router.register('permission/perms',perms.PermsView,base_name='perms')
router.register('orders',orders.OrdersView,base_name='orders')
router.register('skus/images',images.ImageView,base_name='images')
router.register('goods/brands',brands.BrandsView,base_name='brands')
router.register('goods/channels',channels.ChannelView,base_name='channels')
router.register('skus',skus.SkusView,base_name='skus')
router.register('goods/specs',specs.SpecView,base_name='specs')
router.register('goods',goods.SPUView,base_name='goods')
router.register('specs/options',options.OptionsView,base_name='options')
router.register('permission/groups',groups.GroupView,base_name='groups')
pprint(router.urls)
urlpatterns += router.urls
