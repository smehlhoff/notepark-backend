from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        return self.get(username__iexact=username)
