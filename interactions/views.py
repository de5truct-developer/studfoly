from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Comment, Like, Bookmark
from portfolio.models import Project


@require_POST
@login_required
def add_comment(request):
    project_id = request.POST.get('project_id')
    text = request.POST.get('text', '').strip()
    parent_id = request.POST.get('parent_id')

    if not project_id or not text:
        return JsonResponse(
            {'status': 'error', 'message': 'Заполните текст комментария'},
            status=400
        )

    project = get_object_or_404(Project, pk=project_id)
    parent = None
    if parent_id:
        parent = get_object_or_404(Comment, pk=parent_id)

    comment = Comment.objects.create(
        user=request.user,
        project=project,
        text=text,
        parent=parent
    )

    avatar_url = ''
    if hasattr(request.user, 'profile') and request.user.profile.avatar:
        avatar_url = request.user.profile.avatar.url

    return JsonResponse({
        'status': 'ok',
        'comment': {
            'id': comment.id,
            'text': comment.text,
            'user': request.user.get_full_name() or request.user.username,
            'username': request.user.username,
            'avatar_url': avatar_url,
            'created_at': comment.created_at.strftime('%d.%m.%Y %H:%M'),
            'parent_id': parent_id,
        }
    })


@require_POST
@login_required
def delete_comment(request):
    comment_id = request.POST.get('comment_id')
    comment = get_object_or_404(Comment, pk=comment_id, user=request.user)
    comment.delete()
    return JsonResponse({'status': 'ok'})


@require_POST
@login_required
def toggle_like(request):
    project_id = request.POST.get('project_id')
    project = get_object_or_404(Project, pk=project_id)

    like, created = Like.objects.get_or_create(
        user=request.user, project=project
    )
    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        'status': 'ok',
        'liked': liked,
        'likes_count': project.likes.count(),
    })


@require_POST
@login_required
def toggle_bookmark(request):
    project_id = request.POST.get('project_id')
    project = get_object_or_404(Project, pk=project_id)

    bookmark, created = Bookmark.objects.get_or_create(
        user=request.user, project=project
    )
    if not created:
        bookmark.delete()
        bookmarked = False
    else:
        bookmarked = True

    return JsonResponse({
        'status': 'ok',
        'bookmarked': bookmarked,
    })


@login_required
def bookmarks_list(request):
    bookmarks = Bookmark.objects.filter(
        user=request.user
    ).select_related('project', 'project__user', 'project__user__profile')
    return render(request, 'interactions/bookmarks.html', {
        'bookmarks': bookmarks,
    })
