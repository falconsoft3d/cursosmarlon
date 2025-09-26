from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .models import Category, Course, Module, Lesson, Enrollment, Review
from .forms import CategoryForm
# --- CRUD Categorías ---
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'cursos/category_list_admin.html', {'categories': categories})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada correctamente.')
            return redirect('category_list_admin')
    else:
        form = CategoryForm()
    return render(request, 'cursos/category_form.html', {'form': form})

def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada correctamente.')
            return redirect('category_list_admin')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'cursos/category_form.html', {'form': form, 'category': category})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Categoría eliminada correctamente.')
        return redirect('category_list_admin')
    return render(request, 'cursos/category_confirm_delete.html', {'category': category})
from payments.models import Cart, CartItem
from .forms import CourseForm, ModuleForm, LessonForm
import json


def home(request):
    """
    Vista principal del sitio
    """
    featured_courses = Course.objects.filter(status='published', is_featured=True)[:6]
    categories = Category.objects.filter(is_active=True)[:8]
    latest_courses = Course.objects.filter(status='published').order_by('-created_at')[:8]
    context = {
        'featured_courses': featured_courses,
        'categories': categories,
        'latest_courses': latest_courses,
    }
    return render(request, 'cursos/home.html', context)

def course_list(request):
    """
    Lista de cursos con filtros
    """
    courses = Course.objects.filter(status='published')
    categories = Category.objects.filter(is_active=True)
    
    # Filtros
    category_slug = request.GET.get('category')
    difficulty = request.GET.get('difficulty')
    search = request.GET.get('search')
    
    if category_slug:
        courses = courses.filter(category__slug=category_slug)
    
    if difficulty:
        courses = courses.filter(difficulty=difficulty)
    
    if search:
        courses = courses.filter(title__icontains=search)
    
    # Paginación
    paginator = Paginator(courses, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_slug,
        'selected_difficulty': difficulty,
        'search_query': search,
    }
    return render(request, 'cursos/course_list.html', context)

def course_detail(request, slug):
    """
    Detalle de un curso
    """
    course = get_object_or_404(Course, slug=slug, status='published')
    modules = course.modules.all().order_by('order')
    reviews = course.reviews.all()[:5]
    
    # Verificar si el usuario está inscrito
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
    
    # Obtener lecciones gratuitas
    free_lessons = Lesson.objects.filter(module__course=course, is_free=True)
    
    context = {
        'course': course,
        'modules': modules,
        'reviews': reviews,
        'is_enrolled': is_enrolled,
        'free_lessons': free_lessons,
    }
    return render(request, 'cursos/course_detail.html', context)


@login_required
@csrf_exempt
def submit_review(request):
    """
    Enviar reseña de curso
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        course_id = data.get('course_id')
        rating = data.get('rating')
        comment = data.get('comment')
        try:
            course = Course.objects.get(id=course_id)
            if not Enrollment.objects.filter(student=request.user, course=course).exists():
                return JsonResponse({'error': 'Debes estar inscrito en el curso para reseñar'}, status=400)
            review, created = Review.objects.update_or_create(
                course=course,
                student=request.user,
                defaults={
                    'rating': rating,
                    'comment': comment
                }
            )
            return JsonResponse({'success': True, 'message': 'Reseña enviada correctamente'})
        except Course.DoesNotExist:
            return JsonResponse({'error': 'Curso no encontrado'}, status=404)
    return JsonResponse({'error': 'Método no permitido'}, status=405)
def course_player(request, slug):
    """
    Reproductor de curso para estudiantes inscritos
    """
    course = get_object_or_404(Course, slug=slug, status='published')
    enrollment = get_object_or_404(Enrollment, student=request.user, course=course)
    
    # Obtener lección actual
    lesson_id = request.GET.get('lesson')
    current_lesson = None
    
    if lesson_id:
        current_lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course)
    else:
        # Primera lección del curso
        first_module = course.modules.first()
        if first_module:
            current_lesson = first_module.lessons.first()
    
    modules = course.modules.all().order_by('order')
    
    context = {
        'course': course,
        'enrollment': enrollment,
        'current_lesson': current_lesson,
        'modules': modules,
    }
    return render(request, 'cursos/course_player.html', context)

@login_required
@csrf_exempt
def add_to_cart(request):
    """
    Añadir curso al carrito
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        course_id = data.get('course_id')
        
        try:
            course = Course.objects.get(id=course_id, status='published')
            # Verificar si ya está inscrito
            if Enrollment.objects.filter(student=request.user, course=course).exists():
                return JsonResponse({'error': 'Ya estás inscrito en este curso'}, status=400)
            # Si el curso es gratis, inscribir automáticamente
            if course.is_free:
                Enrollment.objects.create(student=request.user, course=course)
                return JsonResponse({'success': True, 'message': '¡Curso gratis agregado a tus cursos!'})
            # Obtener o crear carrito
            cart, created = Cart.objects.get_or_create(user=request.user)
            # Verificar si ya está en el carrito
            if CartItem.objects.filter(cart=cart, course=course).exists():
                return JsonResponse({'error': 'El curso ya está en tu carrito'}, status=400)
            # Añadir al carrito
            CartItem.objects.create(cart=cart, course=course)
            return JsonResponse({'success': True, 'message': 'Curso añadido al carrito'})
        except Course.DoesNotExist:
            return JsonResponse({'error': 'Curso no encontrado'}, status=404)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required
def my_courses(request):
    """
    Cursos del usuario
    """
    enrollments = Enrollment.objects.filter(student=request.user).order_by('-enrolled_at')
    
    context = {
        'enrollments': enrollments,
    }
    return render(request, 'cursos/my_courses.html', context)

@login_required

@login_required
def course_list_admin(request):
    courses = Course.objects.all().order_by('-created_at')
    return render(request, 'cursos/course_list_admin.html', {'courses': courses})

@login_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            messages.success(request, 'Curso creado correctamente.')
            return redirect('course_list_admin')
    else:
        form = CourseForm()
    return render(request, 'cursos/course_form.html', {'form': form})

@login_required
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curso actualizado correctamente.')
            return redirect('course_list_admin')
    else:
        form = CourseForm(instance=course)
    return render(request, 'cursos/course_form.html', {'form': form})

@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Curso eliminado correctamente.')
        return redirect('course_list_admin')
    return render(request, 'cursos/course_confirm_delete.html', {'object': course})

# --- CRUD Módulos ---
@login_required
def module_list(request):
    modules = Module.objects.all().order_by('order')
    return render(request, 'cursos/module_list.html', {'modules': modules})

@login_required
def module_create(request):
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Módulo creado correctamente.')
            return redirect('module_list')
    else:
        form = ModuleForm()
    return render(request, 'cursos/module_form.html', {'form': form})

@login_required
def module_update(request, pk):
    module = get_object_or_404(Module, pk=pk)
    if request.method == 'POST':
        form = ModuleForm(request.POST, instance=module)
        if form.is_valid():
            form.save()
            messages.success(request, 'Módulo actualizado correctamente.')
            return redirect('module_list')
    else:
        form = ModuleForm(instance=module)
    return render(request, 'cursos/module_form.html', {'form': form})

@login_required
def module_delete(request, pk):
    module = get_object_or_404(Module, pk=pk)
    if request.method == 'POST':
        module.delete()
        messages.success(request, 'Módulo eliminado correctamente.')
        return redirect('module_list')
    return render(request, 'cursos/module_confirm_delete.html', {'object': module})

@login_required
def lesson_list(request):
    lessons = Lesson.objects.all().order_by('order')
    return render(request, 'cursos/lesson_list.html', {'lessons': lessons})

@login_required
def lesson_create(request):
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lección creada correctamente.')
            return redirect('lesson_list')
    else:
        form = LessonForm()
    return render(request, 'cursos/lesson_form.html', {'form': form})

@login_required
def lesson_update(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lección actualizada correctamente.')
            return redirect('lesson_list')
    else:
        form = LessonForm(instance=lesson)
    return render(request, 'cursos/lesson_form.html', {'form': form})

@login_required
def lesson_delete(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    if request.method == 'POST':
        lesson.delete()
        messages.success(request, 'Lección eliminada correctamente.')
        return redirect('lesson_list')
    return render(request, 'cursos/lesson_confirm_delete.html', {'object': lesson})

# --- Configurar Pagos ---
@login_required
def configurar_pagos(request):
    return render(request, 'cursos/configurar_pagos.html')

# --- Estadísticas ---
@login_required
def estadisticas(request):
    ventas_totales = 0  # Aquí puedes poner la lógica real
    estudiantes_inscritos = 0  # Aquí puedes poner la lógica real
    return render(request, 'cursos/estadisticas.html', {
        'ventas_totales': ventas_totales,
        'estudiantes_inscritos': estudiantes_inscritos,
    })
