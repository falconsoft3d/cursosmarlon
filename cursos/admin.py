from django.contrib import admin
from .models import Category, Course, Module, Lesson, Enrollment, LessonProgress, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'category', 'price', 'difficulty', 'status', 'is_featured', 'created_at')
    list_filter = ('category', 'difficulty', 'status', 'is_featured', 'created_at')
    search_fields = ('title', 'instructor__first_name', 'instructor__last_name')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('title', 'slug', 'short_description', 'description', 'category', 'instructor')
        }),
        ('Multimedia', {
            'fields': ('thumbnail', 'video_preview')
        }),
        ('Precios y Dificultad', {
            'fields': ('price', 'discount_price', 'difficulty', 'duration_hours')
        }),
        ('Contenido', {
            'fields': ('requirements', 'what_you_learn')
        }),
        ('Estado', {
            'fields': ('status', 'is_featured')
        }),
    )

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'is_free')
    list_filter = ('course', 'is_free')
    search_fields = ('title', 'course__title')
    inlines = [LessonInline]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'lesson_type', 'duration_minutes', 'order', 'is_free')
    list_filter = ('lesson_type', 'is_free', 'module__course')
    search_fields = ('title', 'module__title')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'progress', 'enrolled_at', 'completed_at')
    list_filter = ('enrolled_at', 'completed_at', 'course')
    search_fields = ('student__first_name', 'student__last_name', 'course__title')
    readonly_fields = ('enrolled_at',)

@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'lesson', 'completed', 'completed_at')
    list_filter = ('completed', 'completed_at')
    search_fields = ('enrollment__student__first_name', 'enrollment__student__last_name', 'lesson__title')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('course', 'student', 'rating', 'created_at')
    list_filter = ('rating', 'created_at', 'course')
    search_fields = ('course__title', 'student__first_name', 'student__last_name')
