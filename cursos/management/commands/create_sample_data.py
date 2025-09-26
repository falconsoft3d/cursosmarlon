from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from cursos.models import Category, Course, Module, Lesson
from decimal import Decimal

User = get_user_model()

class Command(BaseCommand):
    help = 'Crear datos de ejemplo para la plataforma'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creando datos de ejemplo...'))

        # Crear instructor si no existe
        instructor, created = User.objects.get_or_create(
            email='instructor@cursosmarlon.com',
            defaults={
                'username': 'instructor@cursosmarlon.com',
                'first_name': 'Juan Carlos',
                'last_name': 'Rodriguez',
                'is_instructor': True,
                'bio': 'Instructor experto en desarrollo web con más de 10 años de experiencia.'
            }
        )
        if created:
            instructor.set_password('instructor123')
            instructor.save()
            self.stdout.write(f'Instructor creado: {instructor.email}')

        # Crear categorías
        categories_data = [
            {
                'name': 'Desarrollo Web',
                'slug': 'desarrollo-web',
                'description': 'Cursos de desarrollo frontend y backend',
                'icon': 'code'
            },
            {
                'name': 'Inteligencia Artificial',
                'slug': 'inteligencia-artificial',
                'description': 'Cursos de AI, Machine Learning y Deep Learning',
                'icon': 'robot'
            },
            {
                'name': 'Bases de Datos',
                'slug': 'bases-de-datos',
                'description': 'Cursos de SQL, NoSQL y gestión de datos',
                'icon': 'database'
            },
            {
                'name': 'DevOps',
                'slug': 'devops',
                'description': 'Cursos de Docker, Kubernetes y CI/CD',
                'icon': 'server'
            },
            {
                'name': 'Programación',
                'slug': 'programacion',
                'description': 'Cursos de diferentes lenguajes de programación',
                'icon': 'laptop-code'
            }
        ]

        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Categoría creada: {category.name}')

        # Crear cursos de ejemplo
        courses_data = [
            {
                'title': 'Django para Principiantes',
                'slug': 'django-para-principiantes',
                'short_description': 'Aprende a desarrollar aplicaciones web con Django desde cero',
                'description': 'En este curso completo de Django, aprenderás a crear aplicaciones web modernas desde cero. Cubriremos todos los conceptos fundamentales incluyendo modelos, vistas, templates, formularios y mucho más.',
                'category': categories[0],  # Desarrollo Web
                'price': Decimal('99.99'),
                'discount_price': Decimal('79.99'),
                'difficulty': 'beginner',
                'duration_hours': 25,
                'requirements': 'Conocimientos básicos de Python\nConocimientos básicos de HTML y CSS',
                'what_you_learn': 'Crear aplicaciones web con Django\nManejar bases de datos con ORM\nImplementar autenticación de usuarios\nDeployar aplicaciones en producción',
                'is_featured': True,
            },
            {
                'title': 'React.js Completo',
                'slug': 'reactjs-completo',
                'short_description': 'Domina React.js y crea aplicaciones web interactivas',
                'description': 'Curso completo de React.js donde aprenderás desde los conceptos básicos hasta temas avanzados como Hooks, Context API, React Router y más.',
                'category': categories[0],  # Desarrollo Web
                'price': Decimal('129.99'),
                'difficulty': 'intermediate',
                'duration_hours': 35,
                'requirements': 'Conocimientos de JavaScript ES6+\nConocimientos básicos de HTML y CSS',
                'what_you_learn': 'Componentes y JSX\nState y Props\nHooks de React\nEnrutamiento con React Router',
                'is_featured': True,
            },
            {
                'title': 'Machine Learning con Python',
                'slug': 'machine-learning-python',
                'short_description': 'Introducción práctica al Machine Learning',
                'description': 'Aprende Machine Learning desde cero con Python. Cubriremos algoritmos de clasificación, regresión, clustering y más usando scikit-learn.',
                'category': categories[1],  # IA
                'price': Decimal('149.99'),
                'difficulty': 'intermediate',
                'duration_hours': 40,
                'requirements': 'Python intermedio\nMatemáticas básicas\nEstadística básica',
                'what_you_learn': 'Algoritmos de ML\nPreprocessing de datos\nEvaluación de modelos\nScikit-learn y Pandas',
                'is_featured': False,
            },
            {
                'title': 'PostgreSQL para Desarrolladores',
                'slug': 'postgresql-desarrolladores',
                'short_description': 'Domina PostgreSQL y optimización de consultas',
                'description': 'Curso avanzado de PostgreSQL donde aprenderás desde consultas básicas hasta optimización y administración avanzada.',
                'category': categories[2],  # Bases de Datos
                'price': Decimal('89.99'),
                'difficulty': 'advanced',
                'duration_hours': 20,
                'requirements': 'Conocimientos básicos de SQL\nExperiencia en programación',
                'what_you_learn': 'Consultas avanzadas\nOptimización de queries\nProcedimientos almacenados\nAdministración de BD',
                'is_featured': False,
            },
            {
                'title': 'Docker y Kubernetes',
                'slug': 'docker-kubernetes',
                'short_description': 'Containerización y orquestación moderna',
                'description': 'Aprende Docker y Kubernetes para containerizar y orquestar aplicaciones en producción.',
                'category': categories[3],  # DevOps
                'price': Decimal('119.99'),
                'discount_price': Decimal('99.99'),
                'difficulty': 'intermediate',
                'duration_hours': 30,
                'requirements': 'Conocimientos básicos de Linux\nExperiencia con aplicaciones web',
                'what_you_learn': 'Containerización con Docker\nOrquestación con Kubernetes\nCI/CD pipelines\nDespliegues automatizados',
                'is_featured': True,
            },
        ]

        for course_data in courses_data:
            course, created = Course.objects.get_or_create(
                slug=course_data['slug'],
                defaults={
                    **course_data,
                    'instructor': instructor,
                    'status': 'published'
                }
            )
            if created:
                self.stdout.write(f'Curso creado: {course.title}')
                
                # Crear módulos y lecciones de ejemplo
                modules_data = [
                    {
                        'title': 'Introducción',
                        'description': 'Conceptos fundamentales y configuración del entorno',
                        'lessons': [
                            {'title': 'Bienvenida al curso', 'duration': 5, 'is_free': True},
                            {'title': 'Configuración del entorno', 'duration': 15, 'is_free': True},
                            {'title': 'Primeros pasos', 'duration': 20},
                        ]
                    },
                    {
                        'title': 'Conceptos Básicos',
                        'description': 'Fundamentos necesarios para el desarrollo',
                        'lessons': [
                            {'title': 'Conceptos fundamentales', 'duration': 25},
                            {'title': 'Práctica guiada', 'duration': 30},
                            {'title': 'Ejercicios prácticos', 'duration': 35},
                        ]
                    },
                    {
                        'title': 'Nivel Intermedio',
                        'description': 'Conceptos más avanzados y mejores prácticas',
                        'lessons': [
                            {'title': 'Técnicas avanzadas', 'duration': 40},
                            {'title': 'Mejores prácticas', 'duration': 30},
                            {'title': 'Proyecto práctico', 'duration': 45},
                        ]
                    }
                ]
                
                for i, module_data in enumerate(modules_data):
                    module = Module.objects.create(
                        course=course,
                        title=module_data['title'],
                        description=module_data['description'],
                        order=i + 1
                    )
                    
                    for j, lesson_data in enumerate(module_data['lessons']):
                        Lesson.objects.create(
                            module=module,
                            title=lesson_data['title'],
                            duration_minutes=lesson_data['duration'],
                            order=j + 1,
                            is_free=lesson_data.get('is_free', False),
                            lesson_type='video'
                        )

        self.stdout.write(self.style.SUCCESS('✅ Datos de ejemplo creados correctamente!'))
        self.stdout.write(self.style.SUCCESS('📧 Instructor: instructor@cursosmarlon.com'))
        self.stdout.write(self.style.SUCCESS('🔑 Contraseña: instructor123'))