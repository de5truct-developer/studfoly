from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class SubscriptionPlan(models.Model):
    PLAN_CHOICES = [
        ('free', 'Бесплатный'),
        ('basic', 'Базовый'),
        ('pro', 'Профессиональный'),
    ]

    name = models.CharField('Название', max_length=50, choices=PLAN_CHOICES, unique=True)
    display_name = models.CharField('Отображаемое название', max_length=100)
    price_monthly = models.DecimalField('Цена в месяц (₸)', max_digits=10, decimal_places=0, default=0)
    price_yearly = models.DecimalField('Цена в год (₸)', max_digits=10, decimal_places=0, default=0)
    max_projects = models.PositiveIntegerField('Макс. проектов', default=3)
    max_skills = models.PositiveIntegerField('Макс. навыков', default=5)
    can_message = models.BooleanField('Доступ к сообщениям', default=False)
    priority_support = models.BooleanField('Приоритетная поддержка', default=False)
    custom_domain = models.BooleanField('Свой домен портфолио', default=False)
    analytics = models.BooleanField('Расширенная аналитика', default=False)
    featured_badge = models.BooleanField('Значок PRO', default=False)
    description = models.TextField('Описание', blank=True)
    is_active = models.BooleanField('Активен', default=True)
    order = models.PositiveIntegerField('Порядок отображения', default=0)

    class Meta:
        verbose_name = 'Тарифный план'
        verbose_name_plural = 'Тарифные планы'
        ordering = ['order']

    def __str__(self):
        return self.display_name


class UserSubscription(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активна'),
        ('expired', 'Истекла'),
        ('cancelled', 'Отменена'),
        ('pending', 'Ожидает оплаты'),
    ]

    PERIOD_CHOICES = [
        ('monthly', 'Ежемесячно'),
        ('yearly', 'Ежегодно'),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='subscription',
        verbose_name='Пользователь'
    )
    plan = models.ForeignKey(
        SubscriptionPlan, on_delete=models.SET_NULL, null=True,
        related_name='subscriptions', verbose_name='Тарифный план'
    )
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='active')
    period = models.CharField('Период', max_length=10, choices=PERIOD_CHOICES, default='monthly')
    start_date = models.DateTimeField('Дата начала', auto_now_add=True)
    end_date = models.DateTimeField('Дата окончания', null=True, blank=True)
    auto_renew = models.BooleanField('Автопродление', default=True)
    created_at = models.DateTimeField('Создана', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлена', auto_now=True)

    class Meta:
        verbose_name = 'Подписка пользователя'
        verbose_name_plural = 'Подписки пользователей'

    def __str__(self):
        return f'{self.user.username} — {self.plan}'

    @property
    def is_active(self):
        if self.status != 'active':
            return False
        if self.end_date and self.end_date < timezone.now():
            return False
        return True

    @property
    def days_remaining(self):
        if not self.end_date:
            return 0
        delta = self.end_date - timezone.now()
        return max(0, delta.days)

    def activate(self, period='monthly'):
        self.status = 'active'
        self.period = period
        if period == 'monthly':
            self.end_date = timezone.now() + timedelta(days=30)
        else:
            self.end_date = timezone.now() + timedelta(days=365)
        self.save()


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('completed', 'Завершен'),
        ('failed', 'Ошибка'),
        ('refunded', 'Возврат'),
    ]

    METHOD_CHOICES = [
        ('card', 'Банковская карта'),
        ('kaspi', 'Kaspi Pay'),
        ('halyk', 'Halyk Bank'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='payments',
        verbose_name='Пользователь'
    )
    plan = models.ForeignKey(
        SubscriptionPlan, on_delete=models.SET_NULL, null=True,
        verbose_name='Тарифный план'
    )
    amount = models.DecimalField('Сумма (₸)', max_digits=10, decimal_places=0)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField('Способ оплаты', max_length=20, choices=METHOD_CHOICES, default='card')
    transaction_id = models.CharField('ID транзакции', max_length=100, blank=True)
    period = models.CharField('Период', max_length=10, default='monthly')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    completed_at = models.DateTimeField('Дата завершения', null=True, blank=True)

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['-created_at']

    def __str__(self):
        return f'Платеж #{self.id} — {self.user.username} — {self.amount}₸'

    def complete(self):
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.transaction_id = f'STUB-{self.id}-{timezone.now().strftime("%Y%m%d%H%M%S")}'
        self.save()
