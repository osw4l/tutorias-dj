from django.conf.urls import url, include
from rest_framework import routers
from . import viewsets, views

router = routers.DefaultRouter()
router.register(r'materias', viewsets.MateriaViewSet)
router.register(r'usuarios', viewsets.UsuarioViewSet)
router.register(r'solicitudes', viewsets.SolicitudViewSet)


urlpatterns = [
    url(r'^viewsets/', include(router.urls)),
    url(r'^materias-usuario/', views.MateriasUsuarioList.as_view()),
    url(r'^materia-usuario/(?P<pk>[0-9]+)/', views.MateriasUsuarioList.as_view()),
    url(r'^crear_usuario/', views.UsuarioCreateApiView.as_view())

]