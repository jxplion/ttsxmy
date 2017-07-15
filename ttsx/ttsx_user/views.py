# coding=utf-8
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from models import *
from ttsx_p.models import GoodsInfo
from ttsx_cart.models import OrderMain, OrderDetial
from hashlib import sha1
from datetime import datetime, timedelta


# Create your views here.
def register(request):
    context = {'title':'注册', 'top':'0'}
    return render(request, 'ttsx_user/register.html', context)


def register_handle(requset):
    p = requset.POST
    uname = p.get('user_name')
    upwd = p.get('user_pwd')
    uemail = p.get('user_email')
    s1 = sha1()
    s1.update(upwd)
    upwd_sha1 = s1.hexdigest()
    ui = Userinfo()
    ui.user_name = uname
    ui.user_pwd = upwd_sha1
    ui.user_email = uemail
    ui.save()
    return redirect('/user/login/')


def register_valid(request):
    uname = request.GET.get('user_name')
    num = Userinfo.objects.filter(user_name=uname).count()
    return JsonResponse({'valid': num})


def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {'title':'登录', 'top': '0' , 'uname':uname}
    return render(request, 'ttsx_user/login.html', context)


def login_handle(request):
    #
    p = request.POST
    uname = p.get('user_name')
    upwd = p.get('user_pwd')
    uchecked = p.get('checked','0')

    s1 = sha1()
    s1.update(upwd)
    upwd_sha1 = s1.hexdigest()

    context = {'title':'登录','uname':uname,'upwd':upwd,'top':'0'}
    # 根据用户名查询数据, 返回 []
    ui = Userinfo.objects.filter(user_name=uname)
    if len(ui) == 0:
        # 用户名不存在
        context['name_error'] = '1'
        return render(request, 'ttsx_user/login.html', context)
    else:
        if ui[0].user_pwd == upwd_sha1: # 登录层共
            # 保存登录
            request.session['uid'] = ui[0].id
            request.session['uname'] = uname
            request.session.set_expiry(0)

            # 记住用户名
            path =  request.session.get('url_path', '/user/')
            response = redirect(path)
            if uchecked == '1':
                response.set_cookie('uname', uname, expires=datetime.now() + timedelta(days=7))
            else:
                response.set_cookie('uname', '', max_age=-1)
            return response
        else:
            context['pwd_error'] = '1'
            return render(request, 'ttsx_user/login.html', context)


def yanzheng(fn):
    def inner(request, *args, **kwargs):

        try:
            Userinfo.objects.get(id=request.session['uid'])
            return fn(request, *args, **kwargs)
        except Exception:
            return redirect('/user/login/')
    return inner


@yanzheng
def center(request):
    ui = Userinfo.objects.get(id=request.session.get('uid'))
    gdlist = request.COOKIES.get('scan','').split(',')
    gdlist.pop()
    g_list = []
    for gid in gdlist:
        g_list.append(GoodsInfo.objects.get(id=gid))

    context = {'title':'用户中心','ui':ui, 'glist':g_list}
    return render(request, 'ttsx_user/center.html', context)


@yanzheng
def order(request):
    ui = Userinfo.objects.get(id=request.session['uid'])
    pindex = request.GET.get('p','1')
    orderm = OrderMain.objects.filter(user_id=ui).order_by('-orderdate')
    paginator = Paginator(orderm, 1)
    orderp = paginator.page(pindex)
    plist = []
    if paginator.num_pages < 5:
        plist = orderp
    elif orderp.number < 3:
        plist = range(1,6)
    elif orderp.number > paginator.num_pages-2:
        plist = range(paginator.num_pages-4, paginator.num_pages+1)
    else:
        plist = range(orderp.number-2, orderp.number+3)
    context = {'title':'订单中心','ui':ui, 'orderp':orderp, 'plist':plist}
    return render(request, 'ttsx_user/order.html', context)


@yanzheng
def site(request):
    ui = Userinfo.objects.get(id=request.session['uid'])
    if request.method=='POST':
        post = request.POST
        ui.user_shou = post.get('ushou')
        ui.user_addr = post.get('uaddress')
        ui.user_mailcode = post.get('ucode')
        ui.user_phone = post.get('uphone')
        ui.save()
    context = {'title':'地址','ui':ui}
    return render(request, 'ttsx_user/site.html', context)


def logout(request):
    request.session.flush()
    return redirect('/index/')


def islogin(request):
    res = 0
    if request.session.has_key('uid'):
        res = 1
    return JsonResponse({'islogin':res})