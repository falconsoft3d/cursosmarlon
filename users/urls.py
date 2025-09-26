from django.urls import path
from . import views
from .views import user_create_view, user_list_view

urlpatterns = [
    path('registro/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.profile_view, name='profile'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('cambiar-contraseña/', views.change_password_view, name='change_password'),
    path('dashboard/usuarios/crear/', user_create_view, name='user_create'),
    path('dashboard/usuarios/', user_list_view, name='user_list'),
    path('dashboard/usuarios/<int:user_id>/editar/', views.user_edit_view, name='user_edit'),
    path('dashboard/usuarios/<int:user_id>/eliminar/', views.user_delete_view, name='user_delete'),
]