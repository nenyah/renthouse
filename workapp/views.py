from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render
from django.utils.timezone import now
from django.http import HttpResponse

from .forms import AppointmentForm, LoginForm, RegisterForm
from .models import Appointment, Area, HouseInfo, UserInfo

# 测试
def test(request):
    # 获取所有学校
    context = {}
    area_list = Area.objects.all()
    context['area_list'] = area_list

    context['excellent_house_list'] = get_excellent_house(area_list)


    context['nearest_house_list'] = get_nearest_house(area_list)


    if '清华大学' not in request.POST:
            return render(request,'test.html', context)
    c=request.POST[1]
    return HttpResponse("OK %s" %c)

def get_excellent_house(area_list):
    # 获取优质房源
    # 随机三个学校区域，选出该区域最便宜的房子
    # 暂时用前三个区域模拟
    excellent_house_list = []
    for area in area_list[:3]:
        house_info = {}
        house = HouseInfo.objects.filter(area_to=area.id).prefetch_related("area_to").order_by('rent')[0]
        house_info['id'] = house.id
        house_info['pic_max'] = house.pic_max
        house_info['label'] = house.label
        house_info['area'] = house.area_to.all()[0]
        house_info['houseIntroduce'] = house.houseIntroduce
        excellent_house_list.append(house_info)
    return excellent_house_list

def get_nearest_house(area_list):
    # 获取最近房源
    # 随机三个学校区域，选出该区域最近的房子
    # 暂时用前三个区域模拟
    nearest_house_list = []
    for area in area_list[:3]:
        house_info = {}
        house = HouseInfo.objects.filter(area_to=area.id).prefetch_related("area_to").order_by('distance')[0]
        house_info['id'] = house.id
        house_info['pic_max'] = house.pic_max
        house_info['label'] = house.label
        house_info['area'] = house.area_to.all()[0]
        house_info['houseIntroduce'] = house.houseIntroduce
        nearest_house_list.append(house_info)
    return nearest_house_list


def index(request):
    context = {}

    # 获取所有学校
    area_list = Area.objects.all()
    context['area_list'] = area_list

    context['excellent_house_list'] = get_excellent_house(area_list)


    context['nearest_house_list'] = get_nearest_house(area_list)

    return render(request, 'index.html', context)


def div_list(ls):
    """用于分割9个房屋信息的列表至3个列表"""
    if len(ls) < 3:
        return ls
    elif len(ls) == 0:
        return []
    else:
        ls_return = []
    num = int(len(ls) / 3)
    if len(ls) % 3 == 0:
        for i in range(0, num * 3, 3):
            ls_return.append(ls[i:i+3])
        return ls_return
    else:
        for i in range(0, num*3+1, 3):
            ls_return.append(ls[i:i+3])
        return ls_return

# 列表页
def product_list(request):
    context = {}
    # 搜索框传数值
    area = request.GET.get('area')
    if request.method == 'GET':
        if area is not None:
            Area_ob = Area.objects.filter(id=area)[0].name
            house_info = HouseInfo.objects.filter(area_to=area).order_by('-rent')
            area_num = len(house_info)
        else:
            Area_ob = '全部地区'
            house_info = HouseInfo.objects.all().order_by('-rent')
            area_num = len(house_info)
    elif request.method == 'POST':
        area = request.POST.get('area')
        Area_ob = Area.objects.filter(id=area)[0].name
        house_info = HouseInfo.objects.filter(area_to=area).order_by('-rent')
        area_num = len(house_info)
        print(area)
    context['area'] = Area_ob
    context['area_num'] = area_num
    context['house_info'] = house_info
    return render(request, 'list.html', context)
    # 
    
    # context['house_list'] = house_list
    # context['page_num'] = page_num
    # context['page_range'] = page_range
    # context['house_list_data'] = house_list_data
    # context['obj_list'] = obj_list
    # context['house_info_list'] = house_info_list

    # return render(request, 'list.html', context)
# 列表页（简单负责）
# @login_required(login_url='/index/')
# def product_list(request):
#     """
#     列表页视图，由简单编写
#     """
#     context = {}
#     area = request.GET.get('area')
#     obj_list = ['价格升序', '价格降序']
#     values = request.GET.getlist('jiage')
#     Area_object = Area.objects.filter(name=area)
#     # print values
#     # print area
#     if request.method == 'GET':  # 直接返回页面

#         house_info = HouseInfo.objects.filter(area_to=Area_object).order_by('-rent')
#     if request.method == 'POST':  # 获取post的值，直接返回查询结果，没有使用django的form表单，未做价格判断，因为js可以直接判断前端输入价格是否正确
#         chuzhu_type = request.POST.get("frequency")
#         housetype = request.POST.getlist("example")
#         rent = request.POST.getlist("rent")
#         rent = [int(i) for i in rent]
#         installations = request.POST.getlist("example1")
#         Area_object = Area.objects.filter(name=area)
#         if housetype:
#             house_info_post = HouseInfo.objects.filter(area_to=Area_object).filter(type=chuzhu_type).filter(
#                 Q(rent__gte=rent[0]) & Q(rent__lte=rent[1])).filter(housetype__in=housetype)
#         else:
#             house_info_post = HouseInfo.objects.filter(area_to=Area_object).filter(type=chuzhu_type).filter(
#                 Q(rent__gte=rent[0]) & Q(rent__lte=rent[1]))
#         if installations:
#             if len(installations) == 1:
#                 house_info = house_info_post.filter(Q(installations__contains=installations[0]))
#             if len(installations) == 2:
#                 house_info = house_info_post.filter(Q(installations__contains=installations[0]) | Q(installations__contains=installations[1]))
#             if len(installations) == 3:
#                 house_info = house_info_post.filter(Q(installations__contains=installations[0]) | Q(installations__contains=installations[1]) | Q(installations__contains=installations[2]))
#             if len(installations) == 4:
#                 house_info = house_info_post.filter(
#                     Q(installations__contains=installations[0]) | Q(installations__contains=installations[1]) | Q(
#                         installations__contains=installations[2]) | Q(installations__contains=installations[3]))
#             if len(installations) == 5:
#                 house_info = house_info_post.filter(
#                     Q(installations__contains=installations[0]) | Q(installations__contains=installations[1]) | Q(
#                         installations__contains=installations[2]) | Q(installations__contains=installations[3]) | Q(installations__contains=installations[4]))
#             if len(installations) == 6:
#                 house_info = house_info_post.filter(
#                     Q(installations__contains=installations[0]) | Q(installations__contains=installations[1]) | Q(
#                         installations__contains=installations[2]) | Q(installations__contains=installations[3]) | Q(installations__contains=installations[4])| Q(installations__contains=installations[5]))
#             if len(installations) == 7:
#                 house_info = house_info_post.filter(
#                     Q(installations__contains=installations[0]) | Q(installations__contains=installations[1]) | Q(
#                         installations__contains=installations[2]) | Q(installations__contains=installations[3]) | Q(installations__contains=installations[4]) | Q(installations__contains=installations[5])| Q(installations__contains=installations[6]))
#             if len(installations) == 8:
#                 house_info = house_info_post.filter(
#                     Q(installations__contains=installations[0]) | Q(installations__contains=installations[1]) | Q(
#                         installations__contains=installations[2]) | Q(installations__contains=installations[3])| Q(installations__contains=installations[4]) | Q(installations__contains=installations[5]) | Q(installations__contains=installations[6]) | Q(installations__contains=installations[7]))
#         else:
#             house_info = house_info_post

#     page_robot = Paginator(house_info, 9)
#     page_num = request.GET.get('page')
#     page_range = page_robot.page_range

#     try:
#         house_info_list = page_robot.page(page_num)
#     except EmptyPage:
#         house_info_list = page_robot.page(page_robot.num_pages)
#     except PageNotAnInteger:
#         house_info_list = page_robot.page(1)
#     area_num = len(house_info)

#     house_list = div_list(house_info_list)
#     try:
#         if type(house_list[0]) != list:
#             house_list = []
#             house_list_data = house_info_list
#     except:
#         house_list_data = []
#         # return HttpResponse('没有结果')

#     context['area'] = area
#     context['area_num'] = area_num
#     context['house_list'] = house_list
#     context['page_num'] = page_num
#     context['page_range'] = page_range
#     context['house_list_data'] = house_list_data
#     context['obj_list'] = obj_list
#     context['house_info_list'] = house_info_list

    # return render(request, 'list.html', context)



# @login_required(login_url='/index/')
def detail(request, id):
    try:
        houseinfo = HouseInfo.objects.get(id=id)
        context = {}
        context['mianji'] = houseinfo.house.split(',')[0]
        context['louceng'] = houseinfo.house.split(',')[1]
        context['zhuangxiu'] = houseinfo.house.split(',')[2]
        context['chaoxiang'] = houseinfo.house.split(',')[3]
        context['zhuzhaileixing'] = houseinfo.house.split(',')[4]
        context['installations'] = houseinfo.installations.split(',')
        context['houseinfo'] = houseinfo
        return render(request, 'detail.html', context)
    except ObjectDoesNotExist:
        return redirect(to='index')


def userinfo(request):
    user = request.user
    appoint_list = user.appoint_u.all()
    context = {"appoint_list":appoint_list}
    return render(request, 'personcenter.html', context)


# 登录页（一凡负责）
def login_view(request):
    context = {}
    if request.method != 'POST':
        form = LoginForm
    else:
        email = request.POST['email']
        user = UserInfo.objects.filter(email=email)
        if user:
            username = user[0].belong_to.username
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect(to='index')
        context['error_message'] = u'你输入的邮箱或密码错误'
        form = LoginForm(request.POST)
    context['form'] = form
    return render(request, 'login.html', context)


# 注册页（一凡负责）
def register(request):
    context = {}
    if request.method != 'POST':
        form = RegisterForm
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User(username=username)
            user.set_password(password)
            user.save()
            user_info = UserInfo(belong_to=user, email=email)
            user_info.save()
            return redirect(to='login')
    context['form'] = form
    return render(request, 'register.html', context)

def forgetpass(request):
    context = {}
    if request.method != "POST":
        pass
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = UserInfo.objects.get(email=username)
            user.belong_to.set_password(password)
            user.belong_to.save()
            user.save()
            tips = u'修改密码成功，点击回到登录页面'
            context['tips'] = tips
        except:
            tips = u'账户不对'
            context['tips'] = tips
    return render(request, 'forgetpass.html', context)


def alteruser(request):
    context = {}
    if request.method != "POST":
        userinfo = request.user.user_info
        context["userinfo"]=userinfo
    else:
        username = request.POST.get('username',"")
        password = request.POST.get('password',"")
        print(username,password)
        user = request.user
        userinfo = request.user.user_info
        userinfo.name = username
        user.set_password(password)
        userinfo.save()
        user.save()
        tips = u'修改密码成功，请重新登录'
        context['tips'] = tips

    return render(request, 'personmodify.html', context)


def appointment(request):
    context = {}
    if request.method != "POST":
        form = AppointmentForm
    else:
        form = AppointmentForm(request.POST)
        if form.is_valid():
            yyname = form.cleaned_data["yyname"]
            yyphone = form.cleaned_data["yyphone"]
            houseinfo_id = request.GET.get('houseinfo_id')
            houseinfo_object = HouseInfo.objects.get(id = houseinfo_id)
            c = Appointment(yyname=yyname, yyphone=yyphone,userinfo=request.user,houseinfo=houseinfo_object)
            c.save()
            return redirect(to="userinfo")
    context['form'] = form
    return render(request, 'appointment.html', context)
