from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Caso, Intervencion
from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from .forms import CasoForm

# Listar Casos (Con restricción de visibilidad)
class CasoListView(LoginRequiredMixin, ListView):
    model = Caso
    # AQUÍ ESTABA EL ERROR DE LA CARPETA "casos":
    template_name = 'soporte/lista_casos.html' 
    context_object_name = 'casos'

    def get_queryset(self):
        user = self.request.user
        # SI ES SOPORTE: Solo ve los casos donde él es el 'soporte' asignado
        if user.groups.filter(name='Soporte').exists():
            return Caso.objects.filter(soporte=user)
            
        # SI ES STAFF (SUPERUSER): Ve todo (opcional, útil para el jefe)
        elif user.is_superuser:
            return Caso.objects.all()
            
        # SI ES CLIENTE: Solo ve sus propios casos
        else:
            return Caso.objects.filter(cliente=user)

# Crear Caso (Cualquier usuario autenticado puede abrir un caso, o solo clientes según decidas)
class CasoCreateView(LoginRequiredMixin, CreateView):
    model = Caso
    form_class = CasoForm  # <--- Usamos form_class en lugar de fields
    template_name = 'soporte/crear_caso.html'
    success_url = reverse_lazy('lista_casos')

    def form_valid(self, form):
        form.instance.cliente = self.request.user
        return super().form_valid(form)

# Crear Intervención (Solo para Técnicos/Soporte)
class IntervencionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Intervencion
    fields = ['caso', 'notas']
    template_name = 'soporte/crear_intervencion.html'
    success_url = reverse_lazy('lista_casos')
    
    # Validación de Rol
    def test_func(self):
        return self.request.user.groups.filter(name='Soporte').exists() or self.request.user.is_staff

    def form_valid(self, form):
        form.instance.tecnico = self.request.user
        try:
            return super().form_valid(form)
        except ValidationError as e:
            form.add_error(None, e) # Muestra el error de la regla de negocio en el template
            return self.form_invalid(form)

class CasoDetailView(LoginRequiredMixin, DetailView):
    model = Caso
    template_name = 'soporte/detalle_caso.html'
    context_object_name = 'caso'

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        
        if user.is_superuser:
            return qs
            
        # Filtro de seguridad:
        # El usuario puede ver el caso SI:
        # es el dueño (cliente) O es el técnico asignado (soporte)
        return qs.filter(Q(cliente=user) | Q(soporte=user))

# Esta función verifica si el usuario es Staff o del grupo Soporte
def es_soporte(user):
    return user.is_staff or user.groups.filter(name='Soporte').exists()

@login_required
@user_passes_test(es_soporte)
def cerrar_caso(request, pk):
    caso = get_object_or_404(Caso, pk=pk)
    
    if caso.estado == 'ABIERTO':
        caso.estado = 'CERRADO'
        caso.save()
        
    return redirect('detalle_caso', pk=pk)


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')  # Al registrarse, lo mandamos al login
    template_name = 'registration/signup.html'