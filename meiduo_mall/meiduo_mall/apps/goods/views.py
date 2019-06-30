import json

from django.shortcuts import render
from django.views import View
from meiduo_mall.utils.categories import get_categories
from .models import GoodsCategory, SKU, GoodsVisitCount
from django.core.paginator import Paginator
from . import constants
from django import http
from meiduo_mall.utils.response_code import RETCODE
from meiduo_mall.utils.breadcrumb import get_breadcrumb
from django_redis import get_redis_connection
from datetime import date


class ListView(View):
    def get(self, request, category_id, page_num):
        # category_id表示第三级分类的编号
        # page_num表示第n页数据

        # 查询分类数据
        categories = get_categories()

        # 查询第三级分类对象
        cat3 = GoodsCategory.objects.get(pk=category_id)
        breadcrumb = get_breadcrumb(cat3)

        # 排序规则
        sort = request.GET.get('sort', 'default')
        if sort == 'default':
            sort_field = '-sales'
        elif sort == 'price':
            sort_field = 'price'
        elif sort == 'hot':
            sort_field = '-comments'
        else:
            sort_field = '-sales'

        # 热销排行：通过另外一个视图实现
        # 查询当前页的商品数据
        # 1.查询指定分类的数据
        skus = SKU.objects.filter(category_id=category_id, is_launched=True).order_by(sort_field)
        # 2.分页
        # 2.1创建分页对象，指定列表、页大小
        paginator = Paginator(skus, constants.SKU_LIST_PER_PAGE)
        # 2.2获取指定页码的数据
        page_skus = paginator.page(page_num)
        # 2.3获取总页数
        total_page = paginator.num_pages

        context = {
            'categories': categories,
            'breadcrumb': breadcrumb,
            'category': cat3,
            'page_skus': page_skus,
            'page_num': page_num,
            'total_page': total_page,
            'sort': sort
        }

        return render(request, 'list.html', context)


class HotView(View):
    def get(self, request, category_id):
        # 查询指定分类的热销商品
        cat3 = GoodsCategory.objects.get(pk=category_id)
        skus = cat3.sku_set.order_by('-sales')[0:2]

        sku_list = []
        for sku in skus:
            sku_list.append({
                'id': sku.id,
                'name': sku.name,
                'price': sku.price,
                'default_image_url': sku.default_image.url
            })

        return http.JsonResponse({
            'code': RETCODE.OK,
            'errmsg': "OK",
            'hot_sku_list': sku_list
        })
class DetailView(View):
    def get(self,request,sku_id):

        try:
            sku = SKU.objects.get(id=sku_id)
        except:
            raise http.Http404("invalid sku code")
        categories = get_categories()
        breadcrumb = get_breadcrumb(sku.category_id)
        spu = sku.spu

        sku_list = spu.skus.all().order_by("id") #skus under same spu
        sku_options = {}  #(options):
        current_sku_options = []
        for each_sku in sku_list:
            sku_specs = each_sku.specs.order_by("spec_id","sku_id") #specification&option infos under one sku
            options = []
            for sku_spec in sku_specs:  # each specification&option record under one sku
                # current_sku_options = []
                options.append(sku_spec.option_id)  #add each option under one sku to options
                if str(sku_id) == str(each_sku.pk):
                    current_sku_options.append(sku_spec.option_id)

            sku_options[tuple(options)] = each_sku.id


        spec_list = []
        # option_list = []  #option_list attach to each spec, sku_id attached to each option

        specs1 = sku.specs.order_by("spec_id") #current sku's specs info
        print(specs1)
        for index,spec_info in enumerate(specs1):

            available_sku_options = current_sku_options[:]  # ( 1,4,7 ) make a new copy of (1,4,7)
            spec_data = spec_info.spec #each spec record in spec table
            spec_options = spec_data.options.order_by("id") #options under specification
            option_list = []  # option_list attach to each spec, sku_id attached to each option
            for option_info in spec_options: #each option under specification
                available_sku_options[index] = option_info.id #update each option's ID in (option1 , option2,..)
                option_info.sku_id = sku_options.get(tuple(available_sku_options), 0)
                # print("available_sku_options",available_sku_options)
                # print("option-sku",option_info,sku_id)
                option_list.append(option_info)
            spec_data.option_list = option_list
            print("each_option_list", spec_data.option_list)
            print("each spec_info in spec_list",spec_data)
            spec_list.append(spec_data)
        print("current sku's specs info",specs1)
        print("spec_list",spec_list)




        context = {
            'sku': sku,
            'categories': categories,
            'breadcrumb': breadcrumb,
            'category_id': sku.category_id,
            'spu': spu,
            'specs':spec_list,
        }
        return render(request, 'detail.html', context)

#
# class DetailView(View):
#     def get(self, request, sku_id):
#         try:
#             sku = SKU.objects.get(pk=sku_id)
#         except:
#             return http.Http404('商品编号无效')
#
#         # 分类数据
#         categories = get_categories()
#
#         # 获取面包屑导航
#         breadcrumb = get_breadcrumb(sku.category)
#
#         # 获取spu
#         spu = sku.spu
#
#         # 获取规格信息：sku===>spu==>specs
#         specs = spu.specs.order_by('id')
#
#         # 查询所有的sku，如华为P10的所有库存商品
#         skus = spu.skus.order_by('id')
#         '''
#         {
#             选项:sku_id
#         }
#         说明：键的元组中，规格的索引是固定的
#         示例数据如下：
#         {
#             (1,3):1,
#             (2,3):2,
#             (1,4):3,
#             (2,4):4
#         }
#         '''
#         sku_options = {}
#         sku_option = []
#         for sku1 in skus:
#             infos = sku1.specs.order_by('spec_id')
#             option_key = []
#             for info in infos:
#                 option_key.append(info.option_id)
#                 # 获取当前商品的规格信息
#                 if sku.id == sku1.id:
#                     sku_option.append(info.option_id)
#             sku_options[tuple(option_key)] = sku1.id
#
#         # 遍历当前spu所有的规格
#         specs_list = []
#         for index, spec in enumerate(specs):
#             option_list = []
#             for option in spec.options.all():
#                 # 如果当前商品为蓝、64,则列表为[2,3]
#                 sku_option_temp = sku_option[:]
#                 # 替换对应索引的元素：规格的索引是固定的[1,3]
#                 sku_option_temp[index] = option.id
#                 # 为选项添加sku_id属性，用于在html中输出链接
#                 option.sku_id = sku_options.get(tuple(sku_option_temp), 0)
#                 # 添加选项对象
#                 option_list.append(option)
#             # 为规格对象添加选项列表
#             spec.option_list = option_list
#             # 重新构造规格数据
#             specs_list.append(spec)
#
#         context = {
#             'sku': sku,
#             'categories': categories,
#             'breadcrumb': breadcrumb,
#             'category_id': sku.category_id,
#             'spu': spu,
#             'specs': specs_list
#         }
#         return render(request, 'detail.html', context)


class DetailVisitView(View):
    def post(self, request, category_id):
        try:
            gvc = GoodsVisitCount.objects.get(category_id=category_id)
        except:
            GoodsVisitCount.objects.create(
                category_id=category_id,
                count=1
            )
        else:
            gvc.count += 1
            gvc.date = date.today()
            gvc.save()
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})


class HistoryView(View):
    def post(self, request):
        # 添加浏览记录
        if not request.user.is_authenticated:
            return http.JsonResponse({'code': RETCODE.USERERR, 'errmsg': '未登录，不记录浏览信息'})
        # 接收
        dict1 = json.loads(request.body.decode())
        sku_id = dict1.get('sku_id')
        # 验证
        if not all([sku_id]):
            return http.JsonResponse({'code': RETCODE.PARAMERR, 'errmsg': '没有商品编号'})

        # 处理：存入redis
        redis_cli = get_redis_connection('history')
        key = 'history_%d' % request.user.id
        # 1.删除列表中的元素
        redis_cli.lrem(key, 0, sku_id)
        # 2.加入最前
        redis_cli.lpush(key, sku_id)
        # 3.截取个数
        redis_cli.ltrim(key, 0, 4)

        # 响应
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})

    def get(self, request):
        if not request.user.is_authenticated:
            return http.JsonResponse({'code': RETCODE.USERERR, 'errmsg': '未登录不查询浏览记录'})

        # 从redis读取当前用户的浏览记录
        redis_cli = get_redis_connection('history')
        sku_ids_bytes = redis_cli.lrange('history_%d' % request.user.id, 0, -1)
        # 注意：从redis中读取的数据为bytes类型，需要转换为int类型
        sku_ids_int = [int(sku_id) for sku_id in sku_ids_bytes]

        # 根据商品编号查询商品对象
        sku_list = []
        for sku_id in sku_ids_int:
            sku = SKU.objects.get(pk=sku_id)
            sku_list.append({
                'id': sku.id,
                'name': sku.name,
                'price': sku.price,
                'default_image_url': sku.default_image.url
            })

        # 响应
        return http.JsonResponse({
            'code': RETCODE.OK,
            'errmsg': "OK",
            'skus': sku_list
        })
