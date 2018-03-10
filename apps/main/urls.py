from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$',
        views.log_in,
        name='entrar'),

    url(r'^salir/',
        views.salir,
        name='salir'),

    url(r'^inicio/',
        views.HomeTemplateView.as_view(),
        name='inicio')
]
