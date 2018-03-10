from rest_framework import serializers
from apps.app import models


class UsuarioSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.ReadOnlyField(source='get_full_name')
    fecha_creacion = serializers.ReadOnlyField(source='get_fecha_creacion')

    class Meta:
        model = models.Usuario
        fields = ('id',
                  'username',
                  'nombre_completo',
                  'descripcion',
                  'direccion',
                  'telefono',
                  'fecha_creacion',
                  'materias')


class MateriaUsuarioSerializer(serializers.ModelSerializer):
    nombre = serializers.ReadOnlyField(source='materia.nombre')
    nombre_tutor = serializers.ReadOnlyField(source='usuario.get_full_name')
    user_tutor = serializers.ReadOnlyField(source='usuario.username')
    descripcion_tutor = serializers.ReadOnlyField(source='usuario.descripcion')
    user_id = serializers.ReadOnlyField(source='usuario.id')

    class Meta:
        model = models.MateriaUsuario
        fields = ('id',
                  'materia',
                  'nombre',
                  'nombre_tutor',
                  'user_id',
                  'user_tutor',
                  'descripcion_tutor',
                  'usuario',
                  'precio')


class MateriaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Materia
        fields = ('id',
                  'nombre',
                  'descripcion',
                  'tutores',
                  )


class SolicitudSerializer(serializers.ModelSerializer):
    nombre_interesado = serializers.ReadOnlyField(source='interesado.get_full_name')
    nombre_tutor = serializers.ReadOnlyField(source='tutor.get_full_name')
    nombre_materia = serializers.ReadOnlyField(source='materia.nombre')

    class Meta:
        model = models.Solicitud
        fields = ('id',
                  'interesado',
                  'nombre_interesado',
                  'tutor',
                  'nombre_tutor',
                  'materia',
                  'nombre_materia',
                  'descripcion',
                  'calificacion',
                  'comentario',
                  'fecha',
                  'hora_inicial',
                  'hora_final',
                  'aprobada',
                  'finalizada'
                  )

