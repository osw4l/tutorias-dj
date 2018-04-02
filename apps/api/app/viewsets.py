from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import status
from apps.utils.shortcuts import get_object_or_none
from .serializers import MateriaSerializer, MateriaUsuarioSerializer, SolicitudSerializer, UsuarioSerializer
from apps.app.models import Materia, MateriaUsuario, Solicitud, Usuario


class MateriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Materia.objects.desarchivados().order_by('nombre')
    serializer_class = MateriaSerializer
    permission_classes = (IsAuthenticated,)

    @detail_route(methods=['get'])
    def tutores(self, request, pk):
        usuarios_materia = MateriaUsuario.objects.filter(
            materia_id=pk,
            oferta_aprobada=True
        ).exclude(
            usuario_id=self.request.user.id
        )
        serializer = MateriaUsuarioSerializer(
            usuarios_materia,
            many=True
        )
        return Response({
            'materia': self.get_object().nombre,
            'descripcion': self.get_object().descripcion,
            'usuarios': serializer.data,
            'tutores': usuarios_materia.count()
        })


class UsuarioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Usuario.objects.filter(is_active=True).exclude(
            id=self.request.user.id
        )

    @detail_route(methods=['get'])
    def materias(self, request, pk):
        materias_usuario = MateriaUsuario.objects.filter(
            usuario_id=pk
        )
        serializer = MateriaUsuarioSerializer(
            materias_usuario,
            many=True
        )
        return Response({
            'usuario': self.get_object().get_full_name(),
            'materias': serializer.data,
            'cantidad_materias': materias_usuario.count()

        })

    @detail_route(methods=['get'])
    def solicitudes(self, request, pk=None):
        solicitudes = Solicitud.objects.filter(
            tutor_id=pk,
            finalizada=True,
            calificacion__gt=0
        )
        serializer = SolicitudSerializer(solicitudes, many=True)
        return Response({
            'solicitudes': serializer.data,
            'cantidad': solicitudes.count()
        })



class SolicitudViewSet(viewsets.ModelViewSet):
    queryset = Solicitud.objects.desarchivados()
    serializer_class = SolicitudSerializer

    def get_data(self, **kwargs):
        kwargs['archivado'] = False
        solicitudes = Solicitud.objects.filter(**kwargs)
        serializer = SolicitudSerializer(solicitudes, many=True)
        return Response({
            'solicitudes': serializer.data,
            'cantidad': solicitudes.count()
        })

    @detail_route(methods=['get'])
    def enviadas(self, request, pk=None):
        return self.get_data(**{
            'interesado': self.request.user.usuario
        })

    @detail_route(methods=['get'])
    def recibidas(self, request, pk=None):
        return self.get_data(**{
            'tutor': self.request.user.usuario
        })

    def get_solicitud(self, **kwargs):
        return get_object_or_none(Solicitud, **kwargs)

    @detail_route(methods=['get'])
    def cancelar(self, request, pk=None):
        return Response({
            'status': self.get_solicitud(**{'pk': pk}).cancelar()
        })

    @detail_route(methods=['get'])
    def aceptar(self, request, pk=None):
        return Response({
            'status': self.get_solicitud(**{'pk': pk}).aprobar()
        })

    @detail_route(methods=['get'])
    def rechazar(self, request, pk=None):
        return Response({
            'status': self.get_solicitud(**{'pk': pk}).rechazar()
        })

    @detail_route(methods=['get'])
    def finalizar(self, request, pk=None):
        return Response({
            'status': self.get_solicitud(**{'pk': pk}).finalizar()
        })

    @detail_route(methods=['get'])
    def archivar(self, request, pk=None):
        return Response({
            'status': self.get_solicitud(**{'pk': pk}).archivar()
        })

    @detail_route(methods=['put'])
    def calificar(self, request, pk=None):
        comentario = request.data['comentario']
        calificacion = request.data['calificacion']
        tutoria = get_object_or_none(Solicitud, id=pk)
        if tutoria:
            tutoria.comentario = comentario
            tutoria.calificacion = int(calificacion)
            tutoria.save(update_fields=['comentario', 'calificacion'])
        return Response({
            'success': True
        })
