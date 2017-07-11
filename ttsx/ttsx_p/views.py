# coding=utf-8
from django.http import JsonResponse
from django.shortcuts import render
from haystack.generic_views import SearchView
from models import *
from django.core.paginator import Paginator
# Create your views here.



def index(request):
    goodslist = []
    # 查询分类对象# 查询最新4个#查询最热门3个
    type_list = TypeInfo.objects.all()
    for t1 in type_list:
        nlist = t1.goodsinfo_set.order_by('-id')[0:4]
        clist = t1.goodsinfo_set.order_by('-gclick')[0:3]
        goodslist.append({'t1':t1,'nlist':nlist,'clist':clist})
    context = {'title':'首页', 'glist':goodslist,'car':'1'}
    return render(request, 'ttsx_p/index.html', context)


def list(request, pindex, porder, pIndex):
    try:
        # 查询分类
        t = TypeInfo.objects.get(id=pindex)
        # 查询最新2个
        nlist = t.goodsinfo_set.order_by('-id')[0:2]
        # 查询全部商品
        # a热门b加个c人气
        if porder == 'a' or porder == '':
            alist = t.goodsinfo_set.order_by('-id')
        elif porder == 'b':
            alist = t.goodsinfo_set.order_by('-gprice')
        elif porder == 'c':
            alist = t.goodsinfo_set.order_by('-gclick')

        p = Paginator(alist, 5)
        # 如果当前没有传递页码信息，则认为是第一页，这样写是为了请求第一页时可以不写页码
        if pIndex == '':
            pIndex = '1'
        pIndex = int(pIndex)
        # if pIndex < 1:
        #     pIndex = 1
        # elif pIndex > p.num_pages:
        #     pIndex = p.num_pages
        alist = p.page(pIndex)
        context = {'title':t.ttitle,
                   'car':'1',
                   'porder':porder ,
                   'nlist':nlist,
                   'alist':alist,
                   't':t,
                   'pIndex':pIndex}
        return render(request, 'ttsx_p/list.html', context)
    except:
        return render(request, '404.html', {'title': 'wu'})


def detail(request, item_num):
    try:
        item = GoodsInfo.objects.get(id=item_num)
        item.gclick += 1  # 人气+1
        item.save()
        t = item.gtype
        nlist = t.goodsinfo_set.order_by('-id')[0:3]
        context = {'title': item.gtitle,
                   'car': '1',
                   'item': item,
                   'nlist': nlist,
                   't': t}
        return render(request, 'ttsx_p/detail.html', context)
    except:
        return render(request, '404.html', {'title':'wu'})


def detailed(request):
    scan = request.COOKIES.get('scan', '').split(',')
    goods_id = request.GET.get('item')
    if goods_id in scan:
        scan.remove(goods_id)
    scan.insert(0, goods_id)
    if len(scan) > 6:
        scan.pop()
    response = JsonResponse({'scan':scan})
    response.set_cookie('scan',','.join(scan), max_age=60*60*24*7)
    print ','.join(scan)
    return response


class MySearchView(SearchView):
    def get_context_data(self, *args, **kwargs):
        context = super(MySearchView, self).get_context_data(*args, **kwargs)
        context['car']='1'
        # page_range = []
        # page = context.get('page_obj')
        # if page.number <= 2:
        #     page_range = range(1, 6)
        # elif page.number >= page.paginator.num_pages - 1:
        #     page_range=range(page.paginator.num_pages-4,page.paginator.num_pages+1)
        # else:
        #     for pindex in page.paginator.num_pages:
        #         if page.number-3 < pindex < page.number+3:
        #             page_range.append(pindex)
        # context['page_range'] = page_range

        return context