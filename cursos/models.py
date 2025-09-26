from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify

class Category(models.Model):
    """
    Modelo para categorías de cursos
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'categories'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Course(models.Model):
    """
    Modelo principal para cursos
    """
    DIFFICULTY_CHOICES = [
        ('beginner', 'Principiante'),
        ('intermediate', 'Intermedio'),
        ('advanced', 'Avanzado'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Borrador'),
        ('published', 'Publicado'),
        ('archived', 'Archivado'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses')
    thumbnail = models.ImageField(upload_to='courses/thumbnails/')
    video_preview = models.FileField(upload_to='courses/previews/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    difficulty = models.CharField(max_length=12, choices=DIFFICULTY_CHOICES, default='beginner')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    duration_hours = models.PositiveIntegerField(help_text="Duración estimada en horas")
    requirements = models.TextField(help_text="Requisitos previos")
    what_you_learn = models.TextField(help_text="Qué aprenderás")
    is_featured = models.BooleanField(default=False)
    is_free = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'courses'
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'slug': self.slug})
    
    @property
    def final_price(self):
        return self.discount_price if self.discount_price else self.price
    
    @property
    def has_discount(self):
        return self.discount_price is not None and self.discount_price < self.price

class Module(models.Model):
    """
    Módulos de un curso
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_free = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'modules'
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Lesson(models.Model):
    """
    Lecciones de un módulo
    """
    LESSON_TYPES = [
        ('video', 'Video'),
        ('text', 'Texto'),
        ('quiz', 'Cuestionario'),
        ('assignment', 'Tarea'),
    ]
    
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    video_file = models.FileField(upload_to='courses/lessons/', blank=True, null=True)
    lesson_type = models.CharField(max_length=10, choices=LESSON_TYPES, default='video')
    duration_minutes = models.PositiveIntegerField(default=0)
    order = models.PositiveIntegerField(default=0)
    is_free = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'lessons'
        verbose_name = 'Lección'
        verbose_name_plural = 'Lecciones'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.module.title} - {self.title}"

class Enrollment(models.Model):
    """
    Inscripciones de estudiantes a cursos
    """
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    progress = models.PositiveIntegerField(default=0)  # Porcentaje de progreso
    
    class Meta:
        db_table = 'enrollments'
        verbose_name = 'Inscripción'
        verbose_name_plural = 'Inscripciones'
        unique_together = ['student', 'course']
    
    def __str__(self):
        return f"{self.student.full_name} - {self.course.title}"

class LessonProgress(models.Model):
    """
    Progreso de lecciones por estudiante
    """
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'lesson_progress'
        verbose_name = 'Progreso de Lección'
        verbose_name_plural = 'Progresos de Lecciones'
        unique_together = ['enrollment', 'lesson']
    
    def __str__(self):
        return f"{self.enrollment.student.full_name} - {self.lesson.title}"

class Review(models.Model):
    """
    Reseñas de cursos
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'reviews'
        verbose_name = 'Reseña'
        verbose_name_plural = 'Reseñas'
        unique_together = ['course', 'student']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.course.title} - {self.rating} estrellas"
