from django.shortcuts import redirect
from django.urls import reverse

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verifica se a URL atual é do Admin
        if request.path.startswith(reverse('admin:index')):
            user = request.user
            
            # Django Admin mandar para o Login
            if not user.is_authenticated:
                return self.get_response(request)

            # Lógica de permissão (Admin, Gestor ou Superuser)
            is_gestor_ou_admin = False
            if user.is_superuser or user.is_staff:
                is_gestor_ou_admin = True
            else:
                try:
                    if user.profile.cargo in ['admin', 'gestor']:
                        is_gestor_ou_admin = True
                except:
                    pass

            # 
            if not is_gestor_ou_admin:
                return redirect('/')

        return self.get_response(request)