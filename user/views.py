
from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, View
# from django.middleware.csrf import _compare_salted_tokens
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.http import HttpResponseRedirect

from user.models import User
from user.forms import UserForm
from user.oauth.providers.naver import NaverMixin
from user.oauth.providers.kakao import KakaoMixin
from toy import settings

# Create your views here.

class UserRegistView(CreateView):
    model = User
    form_class = UserForm
    #fields = ('email', 'name', 'password')#, 'location')\
    success_url = '/para/'
    token = default_token_generator

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.instance:
            self.send_verification_email(form.instance)
        return response

    def send_verification_email(self, user):
        tokens = self.token.make_token(user)
        user.email_user('TEST 입니다.', '인증 주소 : {}/user/{}/{}/'.format(self.request.META.get('HTTP_ORIGIN'), user.pk, tokens), from_email=settings.EMAIL_HOST_USER)
        messages.info(self.request, '이메일 인증 후 로그인 가능합니다.')

    def send_verification_email(self, user):
        tokens = self.token.make_token(user)
        user.email_user('TEST 입니다.', '인증 주소 : {}'.format(self.build_verification_link(user, tokens)), from_email=settings.EMAIL_HOST_USER)
        messages.info(self.request, '이메일 인증 후 로그인 가능합니다.')

    def build_verification_link(self, user, tokens):
        return '{}/user/{}/{}/'.format(self.request.META.get('HTTP_ORIGIN'), user.pk, tokens)

    def form_invalid(self, form):
        messages.error(self.request, 'Failed to Regist_view', extra_tags='danger')
        return super().form_invalid(form)

class UserCheckView(TemplateView):
    model = User
    redirect_url = '/user/login/'
    tokens = default_token_generator

    def get(self, request, *args, **kwargs):
        if self.is_valid_token(**kwargs):
            #user = self.model.objects.get(pk=kwargs.get('pk'))
            messages.info(request, '인증 완료되었습니다.')
        else:
            messages.error(request, '인증 실패하였습니다.')
        return HttpResponseRedirect(self.redirect_url)

    def is_valid_token(self, **kwargs):
        pk = kwargs.get('pk')
        token = kwargs.get('token')
        user = self.model.objects.get(pk=pk)
        valid = self.tokens.check_token(user, token)
        if valid:
            user.is_active = True
            user.save()
        return valid

class UserLoginView(LoginView):
    template_name = 'user/login_form.html'

    def form_invalid(self, form):
        messages.error(self.request, 'Failed to Login_view', extra_tags='danger')
        return super().form_invalid(form)

class UserChangeView(TemplateView):
    template_name = 'user/change_form.html'

class NaverLoginCallbackView(NaverMixin, View):
    success_url = settings.LOGIN_REDIRECT_URL
    failure_url = settings.LOGIN_URL
    required_profiles = ['email', 'name']
    model = User

    def get(self, request, *args, **kwargs):
        provider = kwargs.get('provider')
        csrf_token = request.GET.get('state')
        code = request.GET.get('code')
        is_success, error = self.login_with_naver(csrf_token, code)
        if not is_success:
            messages.error(request, error, extra_tags='danger')
            return HttpResponseRedirect(self.failure_url)
        return HttpResponseRedirect(self.success_url)

        #messages.error(request, 'else_naver', extra_tags='danger')
        #return HttpResponseRedirect(self.failure_url)

    def set_session(self, **kwargs):
        for key, value in kwargs.items():
            self.request.session[key] = value

class KakaoLoginCallbackView(KakaoMixin, View):
    success_url = settings.LOGIN_REDIRECT_URL
    failure_url = settings.LOGIN_URL
    required_profiles = ['email', 'name']
    model = User

    def get(self, request, *args, **kwargs):
        csrf_token = request.GET.get('state')
        code = request.GET.get('code')
        is_success, error = self.login_with_kakao(csrf_token, code)
        if not is_success:
            messages.error(request, error, extra_tags='danger')
            return HttpResponseRedirect(self.failure_url)
        return HttpResponseRedirect(self.success_url)

    def post(self, request, *args, **kwargs):
        csrf_token = request.GET.get('state')
        code = request.GET.get('code')
        is_success, error = self.login_with_kakao(csrf_token, code)
        if not is_success:
            messages.error(request, error, extra_tags='danger')
            return HttpResponseRedirect(self.failure_url)
        return HttpResponseRedirect(self.success_url)

        #messages.error(request, 'else2', extra_tags='danger')
        #return HttpResponseRedirect(self.failure_url)

    def set_session(self, **kwargs):
        for key, value in kwargs.items():
            self.request.session[key] = value