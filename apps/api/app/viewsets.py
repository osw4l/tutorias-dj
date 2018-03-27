from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import status

from apps.api.app.views import CsrfExemptSessionAuthentication
from apps.utils.shortcuts import get_object_or_none
from .serializers import MateriaSerializer, MateriaUsuarioSerializer, SolicitudSerializer, UsuarioSerializer
from apps.app.models import Materia, MateriaUsuario, Solicitud, Usuario


class MateriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Materia.objects.desarchivados().order_by('nombre')
    serializer_class = MateriaSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

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
    authentication_classes = (CsrfExemptSessionAuthentication,)

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


class SolicitudViewSet(viewsets.ModelViewSet):
    queryset = Solicitud.objects.desarchivados()
    serializer_class = SolicitudSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)



