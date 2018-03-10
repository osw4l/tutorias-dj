from django.contrib import admin

from apps.app.forms import UsuarioForm
from . import models
# Register your models here.


admin.site.site_header = 'Tutorias Admin'
admin.site.site_title = 'Tutorias Admin'
admin.site.index_title = 'Tutorias Admin'


@admin.register(models.Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['id', 'creacion', 'username', 'email',
                    'get_full_name', 'direccion', 'telefono',
                    'descripcion', 'archivado']
    form = UsuarioForm


@admin.register(models.Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ['id', 'creacion', 'nombre', 'descripcion', 'archivado']


@admin.register(models.Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ['id', 'creacion', 'descripcion', 'interesado',
                    'tutor', 'materia',
                    'calificacion', 'comentario', 'fecha', 'hora_inicial',
                    'hora_final', 'finalizada',
                    'aprobada', 'archivado']



@admin.register(models.MateriaUsuario)
class MateriaUsuarioAdmin(admin.ModelAdmin):
    list_display = ['id', 'creacion', 'materia',
                    'usuario', 'precio']





