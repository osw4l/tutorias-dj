#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login as auth_login
from django.shortcuts import render, redirect
from django.views.generic import TemplateView


def log_in(request):
    context = {'error': False}
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect('main:inicio')
            else:
                context = {'msj': _('El usuario ha sido desactivado'), 'error': True}
        else:
            context = {'msj': _('usuario o contraseña incorrecta'), 'error': True}

    return render(request, 'sesiones/login.html', context)


@login_required
def salir(request):
    logout(request)
    return redirect('main:entrar')


class HomeTemplateView(TemplateView):
    template_name = 'main/main.html'









