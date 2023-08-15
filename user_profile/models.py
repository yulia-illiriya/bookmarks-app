from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _ 


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username=None, email=None, phone=None, password=None, **extra_fields):
        
        """
        User Manager which are used for our User Model
        """
        if not email:
                raise ValueError('Введите почту')
        email = self.normalize_email(email)


        user = self.model(
                email=email,                
                **extra_fields
            )
        
        if extra_fields.get('is_superuser'):
            user = self.model(
                email=email,                          
                **extra_fields
            )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email=email, password=password, **extra_fields)

    def create_superuser(self, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(
            password=password,
            **extra_fields
        )



class User(AbstractBaseUser, PermissionsMixin):
    
    """Модель, которая отвечает за базового юзера"""
    
    email = models.EmailField(_('email address'), unique=True)    
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    created_at = models.DateTimeField(_('is active'), auto_now_add=True)     

    objects = UserManager()

    USERNAME_FIELD = 'email'    

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

