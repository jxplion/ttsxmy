# coding=utf-8
from django.http import JsonResponse
from django.shortcuts import render
from ttsx_user.views import yanzheng

# Create your views here.
from .models import CartInfo

@yanzheng
def cart(request):
    uid = request.session.get('uid')
    cart_list = CartInfo.objects.filter(user_id=uid)
    context = {'title':'我的购物车','cart_list':cart_list}
    return render(request, 'ttsx_cart/cart.html', context)


def addcart(request):
    try:
        userid = request.session.get('uid')
        itemid = request.GET.get('itemid')
        itemnum = int(request.GET.get('itemnum','1'))
        print type(itemnum)
        cs = CartInfo.objects.filter(user_id=userid, goods_id=itemid)
        if len(cs) > 0:
            c = cs[0]
            c.count += itemnum
        else:
            c = CartInfo()
            c.goods_id = itemid
            c.count = itemnum
            c.user_id = userid
        print userid, itemid, itemnum # 1 41 1
        c.save()
        return  JsonResponse({'isadd':1})
    except:
        return JsonResponse({'isadd': 0})


def countt(request):
    uid = request.session.get('uid')
    cart_count = CartInfo.objects.filter(user_id=uid).count()
    return JsonResponse({'cart_count':cart_count})


def reorder(request):
    return render(request, 'ttsx_cart/reorder.html')