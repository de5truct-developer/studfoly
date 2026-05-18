from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q, Count
from django.utils.text import slugify
import itertools

from .models import Project, ProjectImage, Skill, Education, Experience
from .forms import ProjectForm, SkillForm, EducationForm, ExperienceForm
from accounts.models import UserProfile


def home_view(request):
    query = request.GET.get('q', '')
    city = request.GET.get('city', '')
    skill = request.GET.get('skill', '')
    available_only = request.GET.get('available', '')

    users = User.objects.filter(
        profile__isnull=False
    ).select_related('profile').annotate(
        projects_count=Count('projects')
    )

    if query:
        users = users.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(username__icontains=query) |
            Q(profile__title__icontains=query) |
            Q(profile__bio__icontains=query)
        )
    if city:
        users = users.filter(profile__city__icontains=city)
    if skill:
        users = users.filter(skills__name__icontains=skill).distinct()
    if available_only:
        users = users.filter(profile__is_available=True)

    cities = UserProfile.objects.exclude(
        city=''
    ).values_list('city', flat=True).distinct().order_by('city')

    all_skills = Skill.objects.values_list(
        'name', flat=True
    ).distinct().order_by('name')

    context = {
        'users': users,
        'query': query,
        'city': city,
        'skill': skill,
        'available_only': available_only,
        'cities': cities,
        'all_skills': all_skills,
    }
    return render(request, 'portfolio/home.html', context)


def project_list(request):
    query = request.GET.get('q', '')
    tech = request.GET.get('tech', '')

    projects = Project.objects.select_related('user', 'user__profile').all()

    if query:
        projects = projects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        )
    if tech:
        projects = projects.filter(technologies__icontains=tech)

    all_techs = set()
    for p in Project.objects.values_list('technologies', flat=True):
        for t in p.split(','):
            t = t.strip()
            if t:
                all_techs.add(t)
    all_techs = sorted(all_techs)

    context = {
        'projects': projects,
        'query': query,
        'tech': tech,
        'all_techs': all_techs,
    }
    return render(request, 'portfolio/project_list.html', context)


def project_detail(request, slug):
    project = get_object_or_404(
        Project.objects.select_related('user', 'user__profile'), slug=slug
    )
    gallery = project.images.all()
    comments = project.comments.filter(parent__isnull=True).select_related('user', 'user__profile')

    user_has_liked = False
    user_has_bookmarked = False
    if request.user.is_authenticated:
        user_has_liked = project.likes.filter(user=request.user).exists()
        user_has_bookmarked = project.bookmarks.filter(user=request.user).exists()

    context = {
        'project': project,
        'gallery': gallery,
        'comments': comments,
        'user_has_liked': user_has_liked,
        'user_has_bookmarked': user_has_bookmarked,
        'likes_count': project.likes_count(),
        'comments_count': project.comments_count(),
    }
    return render(request, 'portfolio/project_detail.html', context)


@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            # Ensure unique slug
            if not project.slug:
                project.slug = slugify(project.title)
            original_slug = project.slug
            for i in itertools.count(1):
                if not Project.objects.filter(slug=project.slug).exists():
                    break
                project.slug = f'{original_slug}-{i}'
            project.save()
            messages.success(request, 'Проект успешно создан!')
            return redirect('portfolio:project_detail', slug=project.slug)
    else:
        form = ProjectForm()
    return render(request, 'portfolio/project_form.html', {
        'form': form,
        'title': 'Создать проект',
    })


@login_required
def project_edit(request, slug):
    project = get_object_or_404(Project, slug=slug, user=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Проект успешно обновлён!')
            return redirect('portfolio:project_detail', slug=project.slug)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'portfolio/project_form.html', {
        'form': form,
        'title': 'Редактировать проект',
        'project': project,
    })


@login_required
def project_delete(request, slug):
    project = get_object_or_404(Project, slug=slug, user=request.user)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Проект удалён.')
        return redirect('accounts:dashboard')
    return render(request, 'portfolio/project_confirm_delete.html', {
        'project': project,
    })


@require_POST
@login_required
def add_skill(request):
    form = SkillForm(request.POST)
    if form.is_valid():
        skill = form.save(commit=False)
        skill.user = request.user
        skill.save()
        return JsonResponse({
            'status': 'ok',
            'skill': {
                'id': skill.id,
                'name': skill.name,
                'icon_class': skill.icon_class,
                'percentage': skill.percentage,
                'category': skill.get_category_display(),
            }
        })
    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)


@require_POST
@login_required
def edit_skill(request, pk):
    skill = get_object_or_404(Skill, pk=pk, user=request.user)
    form = SkillForm(request.POST, instance=skill)
    if form.is_valid():
        form.save()
        return JsonResponse({
            'status': 'ok',
            'skill': {
                'id': skill.id,
                'name': skill.name,
                'icon_class': skill.icon_class,
                'percentage': skill.percentage,
                'category': skill.get_category_display(),
            }
        })
    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)


@require_POST
@login_required
def delete_skill(request, pk):
    skill = get_object_or_404(Skill, pk=pk, user=request.user)
    skill.delete()
    return JsonResponse({'status': 'ok'})


@require_POST
@login_required
def add_education(request):
    form = EducationForm(request.POST)
    if form.is_valid():
        edu = form.save(commit=False)
        edu.user = request.user
        edu.save()
        return JsonResponse({'status': 'ok', 'id': edu.id})
    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)


@require_POST
@login_required
def edit_education(request, pk):
    edu = get_object_or_404(Education, pk=pk, user=request.user)
    form = EducationForm(request.POST, instance=edu)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)


@require_POST
@login_required
def delete_education(request, pk):
    edu = get_object_or_404(Education, pk=pk, user=request.user)
    edu.delete()
    return JsonResponse({'status': 'ok'})


@require_POST
@login_required
def add_experience(request):
    form = ExperienceForm(request.POST)
    if form.is_valid():
        exp = form.save(commit=False)
        exp.user = request.user
        exp.save()
        return JsonResponse({'status': 'ok', 'id': exp.id})
    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)


@require_POST
@login_required
def edit_experience(request, pk):
    exp = get_object_or_404(Experience, pk=pk, user=request.user)
    form = ExperienceForm(request.POST, instance=exp)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)


@require_POST
@login_required
def delete_experience(request, pk):
    exp = get_object_or_404(Experience, pk=pk, user=request.user)
    exp.delete()
    return JsonResponse({'status': 'ok'})
