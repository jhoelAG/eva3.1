from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Asignatura, Asistencia
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.db.models import Sum

def index(request):
    return render(request,"index.html")
def pagina_inicio(request):
    return render(request, 'index.html')

# Verificación del rol
def is_lider(user):
    return user.groups.filter(name="Líder").exists()

@login_required
def registrar_asistencia(request):
    if request.method == "POST":
        asignatura_id = request.POST.get("asignatura")
        horas = request.POST.get("horas")
        asignatura = get_object_or_404(Asignatura, id=asignatura_id)

        Asistencia.objects.create(
            asignatura=asignatura,
            usuario=request.user,
            horas=horas,
        )
        asignatura.horas_realizadas += int(horas)
        asignatura.save()
        return redirect("listar_asistencia")

    asignaturas = Asignatura.objects.all()
    return render(request, "registrar_asistencia.html", {"asignaturas": asignaturas})

@login_required
def listar_asistencia(request):
    # Obtener todas las asistencias
    asistencias = Asistencia.objects.all()

    # Consultar si el usuario es líder
    es_lider = request.user.groups.filter(name="Líder").exists()

    # Calcular la suma de horas por asignatura
    horas_por_asignatura = Asistencia.objects.values('asignatura__nombre').annotate(total_horas=Sum('horas'))

    return render(request, "listar_asistencia.html", {
        "asistencias": asistencias,
        "es_lider": es_lider,
        "horas_por_asignatura": horas_por_asignatura,
    })


@login_required
@user_passes_test(is_lider)
def eliminar_asistencia(request, asistencia_id):
    asistencia = get_object_or_404(Asistencia, id=asistencia_id)
    asistencia.delete()
    return redirect("listar_asistencia")

@login_required
@user_passes_test(is_lider)
def agregar_asignatura(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        Asignatura.objects.create(nombre=nombre)
        return redirect("listar_asistencia")

    return render(request, "agregar_asignatura.html")

def custom_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_superuser:
                # Si es un superusuario, redirigir a la página principal en lugar de al admin
                return redirect('pagina_inicio')  # Cambia esto según tu necesidad
            next_url = request.GET.get('next', 'pagina_inicio')
            return redirect(next_url)
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('login')

@login_required
def editar_asistencia(request, asistencia_id):
    if not request.user.groups.filter(name="Líder").exists():
        return redirect('no_tienes_permisos')  # Redirige si el usuario no es líder
    
    asistencia = get_object_or_404(Asistencia, id=asistencia_id)
    asignaturas = Asignatura.objects.all()  # Obtener todas las asignaturas disponibles
    
    if request.method == 'POST':
        nueva_asignatura_id = request.POST.get('asignatura')
        nuevas_horas = request.POST.get('horas')
        
        # Actualizar la asistencia
        asignatura = Asignatura.objects.get(id=nueva_asignatura_id)
        asistencia.asignatura = asignatura
        asistencia.horas = nuevas_horas
        asistencia.save()

        return redirect('listar_asistencia')  # Redirigir al listado de asistencias

    return render(request, 'editar_asistencia.html', {'asistencia': asistencia, 'asignaturas': asignaturas})