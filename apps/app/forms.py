from apps.utils.forms import BaseUserCreationForm
from . import models


class UsuarioForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        model = models.Usuario

