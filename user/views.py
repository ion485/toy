from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, View
# from django.middleware.csrf import _compare_salted_tokens
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.http import HttpResponseRedirect

from user.models import User
from user.oauth.providers.naver import NaverMixin
from user.oauth.providers.kakao import KakaoMixin

# Create your views here.

class UserRegistView(CreateView):
    model = User
    fields = ('email', 'name', 'password')#, 'location')\
    success_url = '/para/'

class UserLoginView(LoginView):
    template_name = 'user/login_form.html'

    def form_invalid(self, form):
        messages.error(self.request, 'Failed to Login', extra_tags='danger')
        return super().form_invalid(form)


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