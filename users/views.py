from django.contrib.auth.decorators import login_required
@login_required
def user_delete_view(request, user_id):
    if not getattr(request.user, 'is_instructor', False):
        return redirect('home')
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Usuario eliminado correctamente.')
        return redirect('user_list')
    return render(request, 'users/user_confirm_delete.html', {'usuario': user})
from django.contrib.auth.decorators import login_required
# Vista para listar usuarios desde el dashboard
@login_required
def user_list_view(request):
    if not getattr(request.user, 'is_instructor', False):
        from django.shortcuts import redirect
        return redirect('home')
    from .models import User
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'users/user_list.html', {'users': users})
# ...existing code...
# Vista para crear usuarios desde el dashboard
@login_required
def user_create_view(request):
    if not getattr(request.user, 'is_instructor', False):
        from django.shortcuts import redirect
        return redirect('home')
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            from django.contrib import messages
            messages.success(request, 'Usuario creado correctamente.')
            return redirect('user_create')
    else:
        form = UserCreateForm()
    return render(request, 'users/user_form.html', {'form': form})

from django.shortcuts import render, redirect, get_object_or_404
@login_required
def user_edit_view(request, user_id):
    if not getattr(request.user, 'is_instructor', False):
        return redirect('home')
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserCreateForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data.get('password'):
                user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Usuario actualizado correctamente.')
            return redirect('user_list')
    else:
        form = UserCreateForm(instance=user)
    return render(request, 'users/user_form.html', {'form': form, 'edit_mode': True, 'usuario': user})
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, UserProfile
from .forms import UserCreateForm
import json
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

def register_view(request):
    """
    Vista de registro de usuario
    """
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        # Validaciones
        if password != password_confirm:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'users/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este email ya está registrado')
            return render(request, 'users/register.html')
        
        # Crear usuario
        user = User.objects.create_user(
            username=email,  # Usar email como username
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Crear perfil
        UserProfile.objects.create(user=user)

        # Login automático
        login(request, user)
        messages.success(request, '¡Registro exitoso! Bienvenido a CursosMarlon')
        return redirect('home')
    return render(request, 'users/register.html')

# Vista para cambiar contraseña
@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Mantener sesión activa
            messages.success(request, 'Tu contraseña ha sido cambiada correctamente.')
            return redirect('profile')
        else:
            messages.error(request, 'Por favor corrige los errores.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {'form': form})

def login_view(request):
    """
    Vista de login
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Email o contraseña incorrectos')
    
    return render(request, 'users/login.html')

@login_required
def logout_view(request):
    """
    Vista de logout
    """
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente')
    from django.http import HttpResponseForbidden
    return redirect('home')

@login_required
def profile_view(request):
    """
    Vista del perfil del usuario
    """
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Actualizar información del usuario
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.bio = request.POST.get('bio')
        if 'avatar' in request.FILES:
            request.user.avatar = request.FILES['avatar']
        request.user.save()
        # Actualizar perfil
        profile.phone = request.POST.get('phone')
        profile.country = request.POST.get('country')
        profile.city = request.POST.get('city')
        profile.website = request.POST.get('website')
        profile.linkedin = request.POST.get('linkedin')
        profile.twitter = request.POST.get('twitter')
        profile.save()
        
        messages.success(request, 'Perfil actualizado correctamente')
        return redirect('profile')
    
    context = {
        'profile': profile,
    }
    return render(request, 'users/profile.html', context)

@login_required
def dashboard_view(request):
    """
    Dashboard del usuario
    """
    # Solo instructores pueden acceder
    if not getattr(request.user, 'is_instructor', False):
        from django.shortcuts import redirect
        return redirect('home')

    from cursos.models import Enrollment
    from payments.models import Order

    # Estadísticas del usuario
    enrollments = Enrollment.objects.filter(student=request.user)
    orders = Order.objects.filter(user=request.user, status='completed')

    recent_courses = enrollments.order_by('-enrolled_at')[:5]
    recent_orders = orders.order_by('-created_at')[:5]

    context = {
        'total_courses': enrollments.count(),
        'completed_courses': enrollments.filter(completed_at__isnull=False).count(),
        'total_orders': orders.count(),
        'recent_courses': recent_courses,
        'recent_orders': recent_orders,
    }
    return render(request, 'users/dashboard.html', context)
