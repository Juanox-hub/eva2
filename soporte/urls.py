from django.urls import path
from .views import CasoListView, CasoCreateView, CasoDetailView, IntervencionCreateView, cerrar_caso, SignUpView

urlpatterns = [
    # EL NAME ES CRÍTICO:
    path('', CasoListView.as_view(), name='lista_casos'), 
    path('crear/', CasoCreateView.as_view(), name='crear_caso'),
    path('<int:pk>/', CasoDetailView.as_view(), name='detalle_caso'),
    path('intervencion/nueva/', IntervencionCreateView.as_view(), name='crear_intervencion'),
    path('cerrar/<int:pk>/', cerrar_caso, name='cerrar_caso'),
    path('signup/', SignUpView.as_view(), name='signup'),
]