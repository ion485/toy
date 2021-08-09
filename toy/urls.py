"""toy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from board.views import hello, paraListView, paraDetailView, paraCUView
from user.views import UserRegistView, UserLoginView, NaverLoginCallbackView, KakaoLoginCallbackView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('hello/<var>', hello),

    path('para/', paraListView.as_view()),
    path('para/create/', paraCUView.as_view()),
    path('para/<para_id>/', paraDetailView.as_view()),
    path('para/<para_id>/update/', paraCUView.as_view()),

    path('user/create/', UserRegistView.as_view()),
    path('user/login/', UserLoginView.as_view()),
    path('user/logout/', LogoutView.as_view()),
    path('user/login/social/naver/callback/', NaverLoginCallbackView.as_view()),
    path('user/login/social/kakao/callback/', KakaoLoginCallbackView.as_view()),

    path('admin/', admin.site.urls),
]
