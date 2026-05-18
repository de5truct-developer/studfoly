from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q

from .models import Conversation, Message
from .forms import MessageForm


@login_required
def inbox_view(request):
    conversations = request.user.conversations.all().order_by('-updated_at')
    conversation_data = []
    for conv in conversations:
        other = conv.get_other_participant(request.user)
        last_msg = conv.get_last_message()
        unread = conv.get_unread_count_for_user(request.user)
        conversation_data.append({
            'conversation': conv,
            'other_user': other,
            'last_message': last_msg,
            'unread_count': unread,
        })
    return render(request, 'messaging/inbox.html', {
        'conversations': conversation_data,
    })


@login_required
def conversation_view(request, conversation_id):
    conversation = get_object_or_404(Conversation, pk=conversation_id)
    if request.user not in conversation.participants.all():
        return redirect('messaging:inbox')

    # Mark messages as read
    conversation.messages.filter(is_read=False).exclude(
        sender=request.user
    ).update(is_read=True)

    msgs = conversation.messages.select_related('sender', 'sender__profile').all()
    other_user = conversation.get_other_participant(request.user)
    form = MessageForm()

    return render(request, 'messaging/conversation.html', {
        'conversation': conversation,
        'messages_list': msgs,
        'other_user': other_user,
        'form': form,
    })


@login_required
def start_conversation(request, username):
    other_user = get_object_or_404(User, username=username)
    if other_user == request.user:
        return redirect('messaging:inbox')

    # Check if conversation already exists
    conversations = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=other_user
    )

    for conv in conversations:
        if conv.participants.count() == 2:
            return redirect('messaging:conversation', conversation_id=conv.pk)

    # Create new conversation
    conversation = Conversation.objects.create()
    conversation.participants.add(request.user, other_user)
    return redirect('messaging:conversation', conversation_id=conversation.pk)


@require_POST
@login_required
def send_message(request):
    conversation_id = request.POST.get('conversation_id')
    text = request.POST.get('text', '').strip()

    if not conversation_id or not text:
        return JsonResponse({'status': 'error', 'message': 'Пустое сообщение'}, status=400)

    conversation = get_object_or_404(Conversation, pk=conversation_id)
    if request.user not in conversation.participants.all():
        return JsonResponse({'status': 'error', 'message': 'Нет доступа'}, status=403)

    msg = Message.objects.create(
        conversation=conversation,
        sender=request.user,
        text=text
    )
    conversation.save()  # Update updated_at

    sender_name = request.user.get_full_name() or request.user.username
    avatar_url = ''
    if hasattr(request.user, 'profile') and request.user.profile.avatar:
        avatar_url = request.user.profile.avatar.url

    return JsonResponse({
        'status': 'ok',
        'message': {
            'id': msg.id,
            'text': msg.text,
            'sender': sender_name,
            'sender_id': request.user.id,
            'avatar_url': avatar_url,
            'created_at': msg.created_at.strftime('%H:%M'),
        }
    })


@login_required
def check_new_messages(request):
    conversation_id = request.GET.get('conversation_id')
    last_id = request.GET.get('last_id', 0)

    if not conversation_id:
        return JsonResponse({'status': 'error'}, status=400)

    conversation = get_object_or_404(Conversation, pk=conversation_id)
    if request.user not in conversation.participants.all():
        return JsonResponse({'status': 'error'}, status=403)

    new_msgs = conversation.messages.filter(
        id__gt=int(last_id)
    ).exclude(sender=request.user).select_related('sender', 'sender__profile')

    # Mark as read
    new_msgs.filter(is_read=False).update(is_read=True)

    messages_data = []
    for msg in new_msgs:
        avatar_url = ''
        if hasattr(msg.sender, 'profile') and msg.sender.profile.avatar:
            avatar_url = msg.sender.profile.avatar.url
        messages_data.append({
            'id': msg.id,
            'text': msg.text,
            'sender': msg.sender.get_full_name() or msg.sender.username,
            'sender_id': msg.sender.id,
            'avatar_url': avatar_url,
            'created_at': msg.created_at.strftime('%H:%M'),
        })

    return JsonResponse({'status': 'ok', 'messages': messages_data})


@login_required
def unread_count(request):
    count = Message.objects.filter(
        conversation__participants=request.user,
        is_read=False
    ).exclude(sender=request.user).count()
    return JsonResponse({'unread_count': count})
