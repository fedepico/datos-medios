from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):
    """
    Mantenedor del usuario.
    """
    
    def create_user(self, username, password=None):
        """
        Crea y guarda un usuario con la contraseña y nickname ingresados.

        Args:
            username (str): Nickname del usuario.
            password (str): Contraseña del usuario.
        
        Returns:
            User: El usuario creado.
        """
        if not username:
           raise ValueError('El usuario debe tener un nickname.')
        user = self.model(username=username)
        user.set_password(password)
        user.is_staff = True
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password):
        """
        Crea y guarda un superusuario con la contraseña y nickname ingresados.

        Args:
            username (str): Nickname del superusuario.
            password (str): Contraseña del superusuario.
        
        Returns:
            User: El superusuario creado.
        """
        user = self.create_user(
           username=username,
           password=password,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """
    Entidad del usario
    """
    id = models.BigAutoField(primary_key=True)
    username = models.CharField('Username', max_length = 15, unique=True)
    password = models.CharField('Password', max_length = 256)
    name = models.CharField('Name', max_length = 30)
    email = models.EmailField('Email', max_length = 100)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    
    def save(self, **kwargs):
        if not self.is_superuser and not self.is_staff:
            some_salt = 'mMUj0DrIK6vgtdIYepkIxN'
            self.password = make_password(self.password, some_salt)
        super().save(**kwargs)

    objects = UserManager()
    USERNAME_FIELD = 'username'