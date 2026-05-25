from django.core.management.base import BaseCommand
from subscriptions.models import SubscriptionPlan


class Command(BaseCommand):
    help = 'Создание тарифных планов по умолчанию'

    def handle(self, *args, **options):
        plans = [
            {
                'name': 'free',
                'display_name': 'Бесплатный',
                'price_monthly': 0,
                'price_yearly': 0,
                'max_projects': 3,
                'max_skills': 5,
                'can_message': False,
                'priority_support': False,
                'custom_domain': False,
                'analytics': False,
                'featured_badge': False,
                'description': 'Базовые возможности для начала работы',
                'order': 0,
            },
            {
                'name': 'basic',
                'display_name': 'Базовый',
                'price_monthly': 990,
                'price_yearly': 9900,
                'max_projects': 15,
                'max_skills': 20,
                'can_message': True,
                'priority_support': False,
                'custom_domain': False,
                'analytics': True,
                'featured_badge': False,
                'description': 'Расширенные возможности для активных пользователей',
                'order': 1,
            },
            {
                'name': 'pro',
                'display_name': 'Профессиональный',
                'price_monthly': 2490,
                'price_yearly': 24900,
                'max_projects': 0,
                'max_skills': 0,
                'can_message': True,
                'priority_support': True,
                'custom_domain': True,
                'analytics': True,
                'featured_badge': True,
                'description': 'Полный доступ ко всем возможностям платформы',
                'order': 2,
            },
        ]

        for plan_data in plans:
            plan, created = SubscriptionPlan.objects.update_or_create(
                name=plan_data['name'],
                defaults=plan_data,
            )
            status = 'создан' if created else 'обновлен'
            self.stdout.write(self.style.SUCCESS(f'План "{plan.display_name}" {status}'))
