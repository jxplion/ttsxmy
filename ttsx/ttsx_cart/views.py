# coding=utf-8
from datetime import datetime
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from ttsx_user.views import yanzheng
from ttsx_user.models import Userinfo

from ttsx_p.models import GoodsInfo
from .models import *
# Create your views here.


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
        gnum = c.count
        return  JsonResponse({'isadd':1,'gnum':gnum})
    except:
        return JsonResponse({'isadd': 0})


def countt(request):
    uid = request.session.get('uid')
    cart_count = CartInfo.objects.filter(user_id=uid).count()
    return JsonResponse({'cart_count':cart_count})


@yanzheng
def reorder(request):
    uid = request.session.get('uid')
    user = Userinfo.objects.get(pk=uid)
    cartlist = request.POST.getlist('cart_id')
    cclist = CartInfo.objects.filter(id__in=cartlist)
    c_ids = ','.join(cartlist)  # 4,5,6
    context = {'title':'提交订单', 'user':user, 'cclist':cclist,'c_ids':c_ids}
    return render(request, 'ttsx_cart/reorder.html', context)


'''
1创建订单表
2请求购物车
3查询请求的商品信息
4查询库存
    5有库存
        1生产详情
        2减去库存
        3计算价钱
        4删除购物车数据
    6没有回滚
'''
@transaction.atomic
def dorder(request):
    isok=True
    sid=transaction.savepoint()
    try:
        uid=request.session.get('uid')
        #1
        now_str=datetime.now().strftime('%Y%m%d%H%M%S')
        main=OrderMain()
        main.orderid='%s%d'%(now_str,uid)
        main.user_id=uid
        main.save()
        #2
        cart_ids=request.POST.get('cart_ids').split(',')
        #3
        cart_list=CartInfo.objects.filter(id__in=cart_ids)
        total=0

        for cart in cart_list:#4
            if cart.count<=cart.goods.gkc:#5
                #5.1
                detail=OrderDetial()
                detail.order=main
                detail.goods=cart.goods
                detail.count=cart.count
                detail.price=cart.goods.gprice
                detail.save()
                #5.2
                cart.goods.gkc-=cart.count
                cart.goods.save()
                #5.3
                total+=cart.count*cart.goods.gprice
                print total
                main.total=total
                print main.total
                main.save()
                #5.4
                cart.delete()
            else:#6
                isok=False
                transaction.savepoint_rollback(sid)
                break
        if isok:
            transaction.savepoint_commit(sid)
    except:
        transaction.savepoint_rollback(sid)
        isok=False

    if isok:
            return redirect('/user/order/')
    else:
            return redirect('/cart/')
'''
def dorder(request):
    uid = request.session.get('uid')
    sid = transaction.savepoint()
    isok = True
    try:
        # 1创建订单表

        tstr = datetime.now().strftime('%Y%m%d%H%M%S')
        main = OrderMain()
        main.orderid = '%s%d' %(tstr, uid)
        main.user_id = uid
        main.status = 0
        main.save()
        # 2请求购物车
        id_all = request.POST.get('id_all').split(',')
        #3查询请求的商品信息
        cart_list = CartInfo.objects.filter(id__in=id_all)
        #4查询库存
        total = 0
        for cart in cart_list:
            # goods = GoodsInfo.objects.get(pk=goods_id)
            if cart.count <= cart.goods.gkc: # 5有库存
                # 1生产详情
                order = OrderDetial()
                order.order = main
                order.goods = cart.goods
                order.count = cart.count
                order.price = cart.goods.gprice
                order.save()
                # 2减去库存
                cart.goods.gkc -= cart.count
                cart.goods.save()
                # 3计算价钱
                total += cart.price*cart.goods.count
                main.total = total
                main.save()
                # 4删除购物车数据
                cart.delete()
            else: #  6没有回滚
                isok = False
                transaction.savepoint_rollback(sid)
                break
        if isok:

            transaction.savepoint_commit(sid)
    except:
        isok = False
        transaction.savepoint_rollback(sid)
    if isok:
        return redirect('/user/order/')
    else:
        return redirect('/cart/')
'''


def del1(request):
    del_id = int(request.GET.get('del_id'))
    cart = CartInfo.objects.get(id=del_id)
    cart.delete()
    return JsonResponse({'isdel':1})