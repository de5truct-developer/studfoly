from django.contrib import admin
from .models import Project, ProjectImage, Skill, Education, Experience


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ('image', 'caption', 'order')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_featured', 'created_date', 'order')
    list_filter = ('is_featured', 'created_date', 'user')
    list_editable = ('is_featured', 'order')
    search_fields = ('title', 'description', 'technologies')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]
    raw_id_fields = ('user',)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'category', 'percentage', 'icon_class')
    list_filter = ('category', 'user')
    search_fields = ('name', 'user__username')


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('institution', 'user', 'degree', 'field_of_study', 'start_date', 'end_date')
    list_filter = ('user',)
    raw_id_fields = ('user',)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('company', 'user', 'position', 'start_date', 'end_date')
    list_filter = ('user',)
    raw_id_fields = ('user',)
