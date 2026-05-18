from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Count

from .forms import UserRegisterForm, UserUpdateForm, UserProfileForm
from .models import UserProfile
from interactions.models import ProfileView, Like
from messaging.models import Message


def register_view(request):
    if request.user.is_authenticated:
        return redirect('portfolio:home')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Добро пожаловать! Ваш аккаунт успешно создан.')
            return redirect('accounts:profile_edit')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('portfolio:home')
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'accounts:dashboard')
            messages.success(request, f'Добро пожаловать, {user.get_full_name() or user.username}!')
            return redirect(next_url)
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из аккаунта.')
    return redirect('portfolio:home')


def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile = get_object_or_404(UserProfile, user=profile_user)
    projects = profile_user.projects.all()
    skills = profile_user.skills.all()
    education = profile_user.education.all()
    experience = profile_user.experience.all()

    # Record profile view
    if request.user.is_authenticated and request.user != profile_user:
        ProfileView.objects.create(viewer=request.user, viewed_profile=profile_user)

    # Skill categories
    skill_categories = (
        skills.values_list('category', flat=True)
        .distinct()
        .order_by('category')
    )
    category_labels = dict(profile_user.skills.model.CATEGORY_CHOICES)

    context = {
        'profile_user': profile_user,
        'profile': profile,
        'projects': projects,
        'skills': skills,
        'education': education,
        'experience': experience,
        'skill_categories': [
            {'key': cat, 'label': category_labels.get(cat, cat)}
            for cat in skill_categories
        ],
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def profile_edit_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль успешно обновлён!')
            return redirect('accounts:profile', username=request.user.username)
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)
    return render(request, 'accounts/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


@login_required
def dashboard_view(request):
    user = request.user
    projects = user.projects.all()
    total_likes = Like.objects.filter(project__user=user).count()
    total_views = ProfileView.objects.filter(viewed_profile=user).count()
    unread_messages = Message.objects.filter(
        conversation__participants=user,
        is_read=False
    ).exclude(sender=user).count()
    recent_comments = []
    for project in projects:
        for comment in project.comments.all()[:5]:
            recent_comments.append(comment)
    recent_comments = sorted(recent_comments, key=lambda x: x.created_at, reverse=True)[:10]

    context = {
        'projects': projects,
        'total_likes': total_likes,
        'total_views': total_views,
        'unread_messages': unread_messages,
        'projects_count': projects.count(),
        'recent_comments': recent_comments,
    }
    return render(request, 'accounts/dashboard.html', context)


@require_POST
@login_required
def toggle_theme(request):
    profile = request.user.profile
    theme = request.POST.get('theme', 'light')
    if theme in ('light', 'dark'):
        profile.theme_preference = theme
        profile.save(update_fields=['theme_preference'])
    return JsonResponse({'status': 'ok', 'theme': profile.theme_preference})
