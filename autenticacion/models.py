from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class ManejadorPersona(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, username,password,**extra_fields):
        if not email:
            raise ValueError("Este email ya está en uso")
        if not username:
            raise ValueError("Este usuario ya está en uso")
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password,**extra_fields):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password=password,
            **extra_fields
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Persona(AbstractBaseUser,PermissionsMixin):

    username            = models.CharField(max_length=10,unique=True,verbose_name="Cédula")
    id_persona          = models.CharField(max_length=10,default="")
    primer_nombre       = models.CharField(max_length=20,)
    segundo_nombre      = models.CharField(max_length=20,null=True,blank=True)
    primer_apellido     = models.CharField(max_length=20)
    segundo_apellido    = models.CharField(max_length=20)
    direccion           = models.CharField(max_length=100)
    telefono            = models.CharField(max_length=12)
    email               = models.EmailField(verbose_name="Email", max_length=60, unique=True)
    date_joined         = models.DateTimeField(verbose_name="Fecha de registro",auto_now_add=True)
    last_login          = models.DateTimeField(verbose_name="Ultima actividad",auto_now=True)
    is_admin            = models.BooleanField(default=False)
    is_active           = models.BooleanField(default=True)
    is_staff            = models.BooleanField(default=False)
    is_superuser        = models.BooleanField(default=False)

    objects = ManejadorPersona()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return "{} - {} {}".format(self.username,self.primer_nombre,self.primer_apellido)

class Localidad(models.Model):
    nombre = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'Localidades'


    def __str__(self):
        return self.nombre

class Abonado(Persona,PermissionsMixin):
    num_medidor         =  models.IntegerField()
    localidad           =  models.ForeignKey(Localidad,on_delete=models.CASCADE)
    latitud             =  models.CharField(max_length=40,blank=True)
    longitud            =  models.CharField(max_length=40,blank=True)

    def __str__(self):
        return super().__str__()

class Oficina(models.Model):
    nombre_oficina = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre_oficina

class Rol(models.Model):
    nombre_rol = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.nombre_rol

class Empleado(Persona,PermissionsMixin):
    rol         = models.ForeignKey(Rol,on_delete=models.CASCADE)
    oficina     = models.ForeignKey(Oficina,on_delete=models.CASCADE)

    def __str__(self):
        return super().__str__()
        