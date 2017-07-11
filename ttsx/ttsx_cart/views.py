# coding=utf-8
from django.http import JsonResponse
from django.shortcuts import render
from ttsx_user.views import yanzheng

# Create your views here.
from .models import CartInfo

@yanzheng
def cart(request):
    context = {'title':'我的购物车',}
    return render(request, 'ttsx_cart/cart.html', context)


def addcart(request):
    userid = request.session.get('uid')
    itemid = request.GET.get('itemid')
    itemnum = request.GET.get('itemnum')
    c = CartInfo()
    c.goods_id_id = itemid
    c.goods_num = itemnum
    c.user_id_id = userid
    c.save()
    return  JsonResponse({'backnum':itemnum})