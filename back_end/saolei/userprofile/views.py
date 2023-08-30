from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from .forms import UserLoginForm, UserRegisterForm, UserRegisterCaptchaForm
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
import json
from django.views.generic import View
# 引入验证登录的装饰器
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from .models import EmailVerifyRecord
from django.core.mail import send_mail
from utils import send_register_email
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import get_user_model
from msuser.models import UserMS

User = get_user_model()


# Create your views here.


def user_login(request):
    if request.method == 'POST':
        # print(request.session.get("login"))
        # print(request.session.keys())
        # print(request.session.session_key)
        # print(request.session.get("_auth_user_id"))
        # print(request.session.get("_auth_user_backend"))
        # print(request.session.get("_auth_user_hash"))
        # print(request.user)

        response = {'status': 100, 'msg': None}

        if request.user.is_authenticated:
            # login(request, request.user)
            response['msg'] = response['msg'] = {"id": request.user.id, "name": request.user.username}
            return JsonResponse(response)
        # if user_id:=request.session.get("_auth_user_id"):
        #     if user:=User.objects.get(id=user_id):
        #         login(request, user)
        #         print(user)
        #         response['msg'] = user.username
        #         return JsonResponse(response)

        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            # print(666)
            # .cleaned_data 清洗出合法数据
            data = user_login_form.cleaned_data
            # 检验账号、密码是否正确匹配数据库中的某个用户
            # 如果均匹配则返回这个 user 对象
            user = authenticate(
                username=data['username'], password=data['password'])
            # print(data)
            # print(user)
            if user:
                # 将用户数据保存在 session 中，即实现了登录动作
                login(request, user)
                # response = http.JsonResponse({"code":0,"errmsg":"注册成功"})
                # response.set_cookie("username",user.username,max_age=3600*24*14)
                response['msg'] = {"id": user.id, "name": user.username}
                return JsonResponse(response)
            else:
                response['status'] = 105
                response['msg'] = "账号或密码输入有误。请重新输入~"
                return JsonResponse(response)
        else:
            response['status'] = 106
            response['msg'] = "账号或密码输入不合法"
            return JsonResponse(response)
    elif request.method == 'GET':
        return HttpResponse("别瞎玩")
        # user_login_form = UserLoginForm()
        # context = {'form': user_login_form}
        # return render(request, 'userprofile/login.html', context)
    else:
        return HttpResponse("别瞎玩")


def user_logout(request):
    logout(request)
    return JsonResponse({'status': 100, 'msg': None})

# @method_decorator(ensure_csrf_cookie)
def user_register(request):
    # print(request)
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        # print(request.POST)
        # print(user_register_form.cleaned_data.get('username'))
        response = {'status': 100, 'msg': None}
        if user_register_form.is_valid():
            emailHashkey = request.POST.get("usertoken", None)
            email_captcha = request.POST.get("email_captcha", None)
            get_email_captcha = EmailVerifyRecord.objects.filter(
                hashkey=emailHashkey).first()
            if get_email_captcha and email_captcha and get_email_captcha.code == email_captcha:
                new_user = user_register_form.save(commit=False)
                # print(new_user)
                # 设置密码(哈希)
                new_user.set_password(
                    user_register_form.cleaned_data['password'])
                new_user.is_active = True # 自动激活
                user_ms = UserMS.objects.create()
                new_user.userms = user_ms
                new_user.save()
                # 保存好数据后立即登录
                login(request, new_user)
                # request.session['login'] = '1'
                # # print(request.session)
                # Jresponse = JsonResponse(response)
                # Jresponse.set_cookie('login','1', max_age=30*24*3600)
                # # print(Jresponse.cookies)
                return JsonResponse(response)
                # return HttpResponse(json.dumps(response), content_type='application/json')
            else:
                response['status'] = 102
                response['msg'] = "邮箱验证码不正确！"
                # print(333)
                return JsonResponse(response)
        else:
            # print(user_register_form.cleaned_data)
            # print(user_register_form.errors)
            response['status'] = 101
            response['msg'] = "显示红色的表单有错误！"
            # print(999)
            return JsonResponse(response)
        
    else:
        return HttpResponse("别瞎玩")

# @login_required(login_url='/userprofile/login/')
# def user_delete(request, id):
#     user = User.objects.get(id=id)
#     # 验证登录用户、待删除用户是否相同
#     if request.user == user:
#         # 退出登录，删除数据并返回博客列表
#         logout(request)
#         user.delete()
#         return redirect("article:article_list")
#     else:
#         return HttpResponse("你没有删除操作的权限。")


# def refresh_captcha(request):
#     to_json_response = dict()
#     to_json_response['status'] = 1  # ajax的状态
#     to_json_response['new_cptch_key'] = CaptchaStore.generate_key()
#     to_json_response['new_cptch_image'] = captcha_image_url(
#         to_json_response['new_cptch_key'])
#     return HttpResponse(json.dumps(to_json_response), content_type='application/json')


# class AjaxCaptchaForm(CreateView):
#     template_name = ''
#     form_class = UserRegisterCaptchaForm

#     def form_invalid(self, form):
#         if self.request.is_ajax():
#             to_json_response = dict()
#             to_json_response['status'] = 0
#             to_json_response['form_errors'] = form.errors

#             to_json_response['new_cptch_key'] = CaptchaStore.generate_key()
#             to_json_response['new_cptch_image'] = captcha_image_url(to_json_response['new_cptch_key'])

#             return HttpResponse(json.dumps(to_json_response), content_type='application/json')

#     def form_valid(self, form):
#         form.save()
#         if self.request.is_ajax():
#             to_json_response = dict()
#             to_json_response['status'] = 1

#             to_json_response['new_cptch_key'] = CaptchaStore.generate_key()
#             to_json_response['new_cptch_image'] = captcha_image_url(to_json_response['new_cptch_key'])

#             return HttpResponse(json.dumps(to_json_response), content_type='application/json')


# 创建验证码
def captcha(request):
    print(666)
    hashkey = CaptchaStore.generate_key()  # 验证码答案
    print(f"?captcha-image={hashkey}")
    # image_url = captcha_image_url(hashkey)  # 验证码地址
    # http://127.0.0.1:8000/userprofile/captcha/image/846d863374767ce04f8949882b05b3b21c697765
    captcha = {'hashkey': hashkey}
    return captcha

# 刷新验证码


def refresh_captcha(request):
    return HttpResponse(json.dumps(captcha(request)), content_type='application/json')

# 验证验证码，若通过，发送email


def get_email_captcha(request):
    if request.method == 'POST':
        # print(666)
        print(request.POST)
        capt = request.POST.get("captcha", None)  # 用户提交的验证码
        key = request.POST.get("hashkey", None)  # 验证码hash
        response = {'status': 100, 'msg': None, "hashkey": None}
        if judge_captcha(capt, key):
            print(777)
            hashkey = send_register_email(request.POST.get("email", None))
            if hashkey:
                response['hashkey'] = hashkey
                return JsonResponse(response)
            else:
                response['status'] = 103
                response['msg'] = "验证码正确，但发送邮件失败"
                return JsonResponse(response)
        else:
            response['status'] = 104
            response['msg'] = "验证码错误"
            return JsonResponse(response)
    else:
        return HttpResponse("只能post。。。")

# 验证验证码


def judge_captcha(captchaStr, captchaHashkey):
    if captchaStr and captchaHashkey:
        get_captcha = CaptchaStore.objects.filter(
            hashkey=captchaHashkey).first()
        if get_captcha and get_captcha.response == captchaStr.lower():
            return True
    return False


# class IndexView(View):
#     def get(self, request):
#         hashkey = CaptchaStore.generate_key()  # 验证码答案
#         image_url = captcha_image_url(hashkey)  # 验证码地址
#         print(hashkey,image_url)
#         captcha = {'hashkey': hashkey, 'image_url': image_url}
#         return render(request, "login.html", locals())

#     def post(self, request):
#         capt = request.POST.get("captcha", None)  # 用户提交的验证码
#         key = request.POST.get("hashkey", None)  # 验证码答案
#         if jarge_captcha(capt, key):
#             return HttpResponse("验证码正确")
#         else:
#             return HttpResponse("验证码错误")