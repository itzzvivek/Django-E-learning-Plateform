from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailBackEnd(ModelBackend):
    def authenticate(self, username=None, Password=None, **kwargs):
        UserModel =get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExits:
            return None
        else:
            if user.check_password(password):
                return user
        return None 