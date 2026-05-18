from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    path('projects/<slug:slug>/edit/', views.project_edit, name='project_edit'),
    path('projects/<slug:slug>/delete/', views.project_delete, name='project_delete'),
    # AJAX endpoints
    path('api/skills/add/', views.add_skill, name='add_skill'),
    path('api/skills/<int:pk>/edit/', views.edit_skill, name='edit_skill'),
    path('api/skills/<int:pk>/delete/', views.delete_skill, name='delete_skill'),
    path('api/education/add/', views.add_education, name='add_education'),
    path('api/education/<int:pk>/edit/', views.edit_education, name='edit_education'),
    path('api/education/<int:pk>/delete/', views.delete_education, name='delete_education'),
    path('api/experience/add/', views.add_experience, name='add_experience'),
    path('api/experience/<int:pk>/edit/', views.edit_experience, name='edit_experience'),
    path('api/experience/<int:pk>/delete/', views.delete_experience, name='delete_experience'),
]
