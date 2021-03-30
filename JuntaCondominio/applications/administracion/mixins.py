from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)

from .models import Corte_mes

class MesDefaulMixin(object):
    mes_cerrado = Corte_mes.objects.get(id=self.kwargs['pk'])
     
    if mes_cerrado.cerrar_mes:
        
