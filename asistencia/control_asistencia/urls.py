from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina_inicio, name='pagina_inicio'),  # Página principal
    path('registrar/', views.registrar_asistencia, name='registrar_asistencia'),
    path('listar/', views.listar_asistencia, name='listar_asistencia'),
    path('eliminar/<int:asistencia_id>/', views.eliminar_asistencia, name='eliminar_asistencia'),
    path('agregar_asignatura/', views.agregar_asignatura, name='agregar_asignatura'),
    path('editar_asistencia/<int:asistencia_id>/', views.editar_asistencia, name='editar_asistencia'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
]
