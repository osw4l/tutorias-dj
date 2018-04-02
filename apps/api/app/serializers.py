from rest_framework import serializers
from apps.app import models
from django.contrib.auth.hashers import make_password


class UsuarioSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.ReadOnlyField(source='get_full_name')
    fecha_creacion = serializers.ReadOnlyField(source='get_fecha_creacion')
    calificacion = serializers.ReadOnlyField(source='get_calificacion')

    class Meta:
        model = models.Usuario
        fields = ('id',
                  'username',
                  'first_name',
                  'last_name',
                  'nombre_completo',
                  'descripcion',
                  'direccion',
                  'telefono',
                  'fecha_creacion',
                  'email',
                  'materias',
                  'password',
                  'calificacion')

    def create(self, validate_data):
        password = make_password(validate_data['password'])
        instance = super().create(validate_data)
        instance.password = password
        instance.save()
        return instance


class MateriaUsuarioSerializer(serializers.ModelSerializer):
    nombre = serializers.ReadOnlyField(source='materia.nombre')
    nombre_tutor = serializers.ReadOnlyField(source='usuario.get_full_name')
    user_tutor = serializers.ReadOnlyField(source='usuario.username')
    descripcion_tutor = serializers.ReadOnlyField(source='usuario.descripcion')
    user_id = serializers.ReadOnlyField(source='usuario.id')
    email_tutor = serializers.ReadOnlyField(source='usuario.email')

    class Meta:
        model = models.MateriaUsuario
        fields = ('id',
                  'materia',
                  'nombre',
                  'nombre_tutor',
                  'user_id',
                  'user_tutor',
                  'email_tutor',
                  'descripcion_tutor',
                  'usuario',
                  'precio',
                  'oferta_aprobada')


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
    nombre_materia = serializers.ReadOnlyField(source='materia.materia.nombre')
    valor = serializers.ReadOnlyField(source='get_valor')
    hora_creacion = serializers.ReadOnlyField(source='get_hora_creacion')
    fecha_creacion = serializers.ReadOnlyField(source='get_fecha_creacion')
    username_interesado = serializers.ReadOnlyField(source='interesado.username')

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
                  'hora',
                  'horas',
                  'creacion',
                  'aprobada',
                  'finalizada',
                  'valor',
                  'rechazada',
                  'cancelada',
                  'hora_creacion',
                  'fecha_creacion',
                  'username_interesado'
                  )

