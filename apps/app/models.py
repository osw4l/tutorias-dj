import locale
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from smart_selects.db_fields import ChainedForeignKey

from apps.utils.shortcuts import get_object_or_none
from . import constants


# Create your models here.

class TutoriaQueryset(models.QuerySet):

    def archive(self):
        return self.filter(archivado=True)

    def all_unarchived(self):
        return self.filter(archivado=False)


class TutoriaModelManager(BaseUserManager):
    def get_queryset(self):
        return TutoriaQueryset(self.model, using=self._db)

    def archivados(self):
        return self.get_queryset().archive().order_by('-id')

    def desarchivados(self):
        return self.get_queryset().all_unarchived().order_by('-id')


class BaseNombre(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        abstract = True

    def __str__(self):
        return self.nombre


class BaseTutoriaModel(models.Model):
    creacion = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    archivado = models.BooleanField(default=False)
    objects = TutoriaModelManager()

    class Meta:
        abstract = True

    def get_fecha_creacion(self):
        locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
        return self.creacion.strftime('%d de %B de %Y')


class Usuario(User, BaseTutoriaModel):
    descripcion = models.TextField(verbose_name='Descripción')
    telefono = models.CharField(max_length=10, unique=True)
    direccion = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def get_materias(self):
        return MateriaUsuario.objects.filter(
            usuario=self
        )

    def materias(self):
        return self.get_materias().count()


class Materia(BaseTutoriaModel, BaseNombre):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()

    class Meta:
        verbose_name = 'Materia'
        verbose_name_plural = 'Materias'

    def get_tutores(self):
        return MateriaUsuario.objects.filter(
            materia_id=self,
            oferta_aprobada=True
        )

    def tutores(self):
        return self.get_tutores().count()


class MateriaUsuario(BaseTutoriaModel):
    materia = models.ForeignKey(Materia)
    usuario = models.ForeignKey(Usuario)
    precio = models.PositiveIntegerField(verbose_name='Precio por hora', default=0)
    oferta_aprobada = models.BooleanField(default=False, editable=False)

    class Meta:
        verbose_name = 'Materia Usuario'
        verbose_name_plural = 'Materias Usuarios'
        unique_together = ['materia', 'usuario']


class Solicitud(BaseTutoriaModel):
    interesado = models.ForeignKey(Usuario, related_name='+')
    tutor = models.ForeignKey(Usuario, related_name='+')
    materia = models.ForeignKey(MateriaUsuario)
    descripcion = models.TextField()
    calificacion = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        blank=True,
        null=True
    )
    comentario = models.TextField(blank=True, null=True)
    fecha = models.DateField()
    hora = models.TimeField()
    horas = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        default=0
    )
    aprobada = models.BooleanField(default=False)
    finalizada = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Solicitud'
        verbose_name_plural = 'Solicitudes'

    def get_valor(self):
        materia = get_object_or_none(
            MateriaUsuario,
            materia=self.materia,
            usuario=self.tutor
        )
        total = 0
        if materia is not None:
            print(materia.materia.nombre)
            print(materia.precio)
            total = materia.precio * self.horas
        return total


