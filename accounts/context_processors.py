from messaging.models import Message


def global_context(request):
    context = {
        'unread_messages_count': 0,
        'current_theme': 'light',
    }

    if request.user.is_authenticated:
        context['unread_messages_count'] = Message.objects.filter(
            conversation__participants=request.user,
            is_read=False
        ).exclude(sender=request.user).count()

        if hasattr(request.user, 'profile'):
            context['current_theme'] = request.user.profile.theme_preference

    return context
