from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import AnonymousUser, AbstractUser

from user.models import User
UserModel = User


class MyBackend(ModelBackend):
    def authenticate(self, request, name=None,**kwargs):
        if name is None:
            name = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel._default_manager.get_by_natural_key(name)
        except UserModel.DoesNotExist:
            pass
        else:
            if self.user_can_authenticate(user):
                return user