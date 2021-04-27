from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import View
#
from .models import User


def check_ocupation_user(ocupation, user_ocupation):
    #
    #print("ocupacio ocupation n===>", ocupation)
    #print("ocupacion user_ocupation ===>", user_ocupation)

    if (ocupation == User.ADMINISTRADOR or ocupation == user_ocupation):
        #print(" variable ", ocupation + "= " + "= " + user_ocupation )
        
        return True
    else:
        #print("variable", ocupation + " =" + "= " + user_ocupation )
        #print("ocupacion user_ocupation ===>", user_ocupation)
        return False


class UsuarioPermisoMixin(LoginRequiredMixin):
    login_url = reverse_lazy('users_app:user-login')

    def dispatch(self, request, *args, **kwargs):
        #print("request.user.is_authenticated ====>",request.user.is_authenticated )
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        #
        #print("request.user.ocupation ===>", request.user.ocupation)
        #print("User.ALMACEN ===>", User.ALMACEN)
        #print("User.ALMACEN ===>", User.VARON)


        if not check_ocupation_user(request.user.ocupation, User.USUARIO):
            # no tiene autorizacion
            return HttpResponseRedirect(
                reverse(
                    'users_app:user-login'
                )
            )

        return super().dispatch(request, *args, **kwargs)


class OtrosPermisoMixin(LoginRequiredMixin):
    login_url = reverse_lazy('users_app:user-login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not check_ocupation_user(request.user.ocupation, User.OTROS):
            # no tiene autorizacion
            return HttpResponseRedirect(
                reverse(
                    'users_app:user-login'
                )
            )
        return super().dispatch(request, *args, **kwargs)


class AdminPermisoMixin(LoginRequiredMixin):
    login_url = reverse_lazy('users_app:user-login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        #
        if not check_ocupation_user(request.user.ocupation, User.ADMINISTRADOR):
            # no tiene autorizacion
            return HttpResponseRedirect(
                reverse(
                    'users_app:user-login'
                )
            )
        return super().dispatch(request, *args, **kwargs)
        
