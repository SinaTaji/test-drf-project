from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, phone_number, password=None):
        if not phone_number:
            raise ValueError('شماره موبایل باید وارد شود')

        user = self.model(
            username=username,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, phone_number, password=None):
        user = self.create_user(username=username, phone_number=phone_number, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
