from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.api.app.serializers import MateriaSerializer, MateriaUsuarioSerializer, UsuarioSerializer, SolicitudSerializer
from apps.app.models import Usuario, MateriaUsuario, Solicitud
from apps.utils.print_colors import _green
from apps.utils.shortcuts import get_object_or_none


class MateriasUsuarioList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        response = {}
        if hasattr(self.request.user, 'usuario'):
            usuario = get_object_or_none(Usuario, id=self.request.user.id)
            serializer = MateriaUsuarioSerializer(usuario.get_materias().order_by('-id'), many=True)
            response = {
                'materias': serializer.data
            }
        else:
            response['error'] = 'Este usuario es administrador y no puede tener materias'
        return Response(response)

    def post(self, request, format=None):
        response = {}
        materia = self.request.data['materia']
        if hasattr(self.request.user, 'usuario') and materia:
            query_args = {
                'usuario_id': self.request.user.id,
                'materia_id': materia
            }
            if MateriaUsuario.objects.filter(**query_args).count() == 0:
                MateriaUsuario.objects.create(**query_args)
                response['success'] = True
            else:
                response['success'] = False
        else:
            response['success'] = False
        return Response(response)

    def delete(self, request, pk, format=None):
        response = {}
        print(pk)
        if hasattr(self.request.user, 'usuario') and pk is not None:
            materia = get_object_or_none(MateriaUsuario, id=pk)
            if materia is not None:
                materia.delete()
                response['success'] = True
            else:
                response['success'] = False
        return Response(response)

    def put(self, request, pk, format=None):
        response = {}
        if hasattr(self.request.user, 'usuario') and pk is not None:
            materia = get_object_or_none(MateriaUsuario, id=pk)
            if materia is not None:
                materia.precio = request.data['precio']
                materia.save(update_fields=['precio'])
                response['success'] = True
            else:
                response['success'] = False
        else:
            response['success'] = False
        return Response(response)


class UsuarioCreateApiView(mixins.CreateModelMixin,
                           generics.GenericAPIView):
    serializer_class = UsuarioSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
