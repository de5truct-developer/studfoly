from django.db import models
from django.contrib.auth.models import User


class Conversation(models.Model):
    participants = models.ManyToManyField(
        User, related_name='conversations', verbose_name='Участники'
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Диалог'
        verbose_name_plural = 'Диалоги'
        ordering = ['-updated_at']

    def __str__(self):
        names = ', '.join(
            u.get_full_name() or u.username
            for u in self.participants.all()[:3]
        )
        return f'Диалог: {names}'

    def get_last_message(self):
        return self.messages.order_by('-created_at').first()

    def get_unread_count_for_user(self, user):
        return self.messages.filter(is_read=False).exclude(sender=user).count()

    def get_other_participant(self, user):
        return self.participants.exclude(pk=user.pk).first()


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name='messages',
        verbose_name='Диалог'
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages',
        verbose_name='Отправитель'
    )
    text = models.TextField('Текст сообщения')
    is_read = models.BooleanField('Прочитано', default=False)
    created_at = models.DateTimeField('Дата отправки', auto_now_add=True)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.sender.username}: {self.text[:50]}'
