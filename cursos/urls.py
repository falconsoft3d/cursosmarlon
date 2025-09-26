from django.urls import path
from . import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cursos/', views.course_list, name='course_list'),
    path('curso/<slug:slug>/', views.course_detail, name='course_detail'),
    path('curso/<slug:slug>/estudiar/', views.course_player, name='course_player'),
    path('mis-cursos/', views.my_courses, name='my_courses'),
    path('api/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('api/submit-review/', views.submit_review, name='submit_review'),

    # CRUD Cursos
    path('dashboard/cursos/', views.course_list_admin, name='course_list_admin'),
    path('dashboard/cursos/crear/', views.course_create, name='course_create'),
    path('dashboard/cursos/<int:pk>/editar/', views.course_update, name='course_update'),
    path('dashboard/cursos/<int:pk>/eliminar/', views.course_delete, name='course_delete'),

    # CRUD Módulos
    path('dashboard/modulos/', views.module_list, name='module_list'),
    path('dashboard/modulos/crear/', views.module_create, name='module_create'),
    path('dashboard/modulos/<int:pk>/editar/', views.module_update, name='module_update'),
    path('dashboard/modulos/<int:pk>/eliminar/', views.module_delete, name='module_delete'),

    # CRUD Lecciones
    path('dashboard/lecciones/', views.lesson_list, name='lesson_list'),
    path('dashboard/lecciones/crear/', views.lesson_create, name='lesson_create'),
    path('dashboard/lecciones/<int:pk>/editar/', views.lesson_update, name='lesson_update'),
    path('dashboard/lecciones/<int:pk>/eliminar/', views.lesson_delete, name='lesson_delete'),

    # CRUD Categorías
    path('dashboard/categorias/', views.category_list, name='category_list_admin'),
    path('dashboard/categorias/crear/', views.category_create, name='category_create'),
    path('dashboard/categorias/<int:pk>/editar/', views.category_update, name='category_update'),
    path('dashboard/categorias/<int:pk>/eliminar/', views.category_delete, name='category_delete'),

    # Configurar Pagos y Estadísticas
    path('dashboard/configurar-pagos/', views.configurar_pagos, name='configurar_pagos'),
    path('dashboard/estadisticas/', views.estadisticas, name='estadisticas'),
]