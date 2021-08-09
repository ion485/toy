from django.conf import settings
from django.contrib.auth import login

from user.models import User

import requests

class KakaoClient:
    client_id = settings.KAKAO_CLIENT_ID
    secret_key = settings.KAKAO_SECRET_KEY
    grant_type = 'authorization_code'

    auth_url = 'https://kauth.kakao.com/oauth/token'
    profile_url = 'https://kapi.kakao.com/v2/user/me'
    redirect_uri = 'http://localhost:8000/user/login/social/kakao/callback/'

    __instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.__instance, cls):
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def get_access_token(self, state, code):
        res = requests.post(self.auth_url, data={'grant_type': self.grant_type, 'client_id': self.client_id, 'redirect_uri': self.redirect_uri, 'code': code, 'client_secret': self.secret_key})
        #res = requests.get(self.auth_url, params={'grant_type': self.grant_type, 'client_id': self.client_id, 'redirect_uri': self.redirect_uri, 'code': code})

        return res.ok, res.json()

    def get_profile(self, access_token, token_type='Bearer'):
        res = requests.get(self.profile_url, headers={'Authorization': '{} {}'.format(token_type, access_token)}).json()
        
        return True, res.get('kakao_account')

class KakaoMixin:
    kakao_client = KakaoClient()

    def login_with_kakao(self, state, code):
        data = User.objects.all()
        
        is_success, token_infos = self.kakao_client.get_access_token(state, code)

        if not is_success:
            #return False, code
            return False, 'access denied'

        token_type = token_infos.get('token_type')
        access_token = token_infos.get('access_token')
        expires_in = token_infos.get('expires_in')
        refresh_token = token_infos.get('refresh_token')

        is_success, profi = self.get_kakao_profile(access_token, token_type)
        if not is_success:
            return False, profi

        profiles = profi.get('profile')
        

        for person in data:
            if person.email == profi.get('email') and person.name == profiles.get('nickname'):
                break
            elif person.name == profiles.get('nickname'):
                return False, '이미 연동된 이름입니다. 연동된 계정 : {}'.format(person.location)
            elif person.email == profiles.get('email'):
                return False, '이미 연동된 이메일입니다.'

        user, created = self.model.objects.get_or_create(email=profi.get('email'))

        if created:
            user.set_password(None)
            user.name = profiles.get('nickname')
        user.location = 'Kakao'
        user.is_active = True
        user.save()
        # else:
        #     return False, '이미 존재하는 계정입니다.'

        login(self.request, user, 'user.oauth.backends.NaverBackend')

        self.set_session(access_token=access_token, refresh_token=refresh_token, expires_in=expires_in, token_type=token_type)

        return True, user

    def get_kakao_profile(self, access_token, token_type):
        is_success, profiles = self.kakao_client.get_profile(access_token, token_type)

        if not is_success:
            return False, 'kkk'

        return True, profiles


