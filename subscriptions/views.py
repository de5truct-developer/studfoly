from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone

from .models import SubscriptionPlan, UserSubscription, Payment


def plans_view(request):
    plans = SubscriptionPlan.objects.filter(is_active=True)
    current_plan = None
    if request.user.is_authenticated:
        sub = getattr(request.user, 'subscription', None)
        if sub and sub.is_active:
            current_plan = sub.plan
    context = {
        'plans': plans,
        'current_plan': current_plan,
    }
    return render(request, 'subscriptions/plans.html', context)


@login_required
def checkout_view(request, plan_name, period='monthly'):
    plan = get_object_or_404(SubscriptionPlan, name=plan_name, is_active=True)

    if plan.name == 'free':
        messages.info(request, 'Бесплатный план не требует оплаты.')
        return redirect('subscriptions:plans')

    amount = plan.price_monthly if period == 'monthly' else plan.price_yearly

    context = {
        'plan': plan,
        'period': period,
        'amount': amount,
        'period_label': 'месяц' if period == 'monthly' else 'год',
    }
    return render(request, 'subscriptions/checkout.html', context)


@require_POST
@login_required
def process_payment_view(request):
    plan_name = request.POST.get('plan')
    period = request.POST.get('period', 'monthly')
    payment_method = request.POST.get('payment_method', 'card')

    plan = get_object_or_404(SubscriptionPlan, name=plan_name, is_active=True)
    amount = plan.price_monthly if period == 'monthly' else plan.price_yearly

    payment = Payment.objects.create(
        user=request.user,
        plan=plan,
        amount=amount,
        payment_method=payment_method,
        period=period,
    )

    payment.complete()

    sub, created = UserSubscription.objects.get_or_create(
        user=request.user,
        defaults={'plan': plan}
    )
    sub.plan = plan
    sub.activate(period=period)

    messages.success(request, f'Подписка «{plan.display_name}» успешно оформлена!')
    return redirect('subscriptions:my_subscription')


@login_required
def my_subscription_view(request):
    sub = getattr(request.user, 'subscription', None)
    payments = Payment.objects.filter(user=request.user)[:10]

    context = {
        'subscription': sub,
        'payments': payments,
    }
    return render(request, 'subscriptions/my_subscription.html', context)


@require_POST
@login_required
def cancel_subscription_view(request):
    sub = getattr(request.user, 'subscription', None)
    if sub and sub.is_active:
        sub.status = 'cancelled'
        sub.auto_renew = False
        sub.save()
        messages.info(request, 'Подписка отменена. Она будет активна до конца оплаченного периода.')
    return redirect('subscriptions:my_subscription')


@require_POST
@login_required
def toggle_auto_renew_view(request):
    sub = getattr(request.user, 'subscription', None)
    if sub:
        sub.auto_renew = not sub.auto_renew
        sub.save()
        status = 'включено' if sub.auto_renew else 'отключено'
        messages.success(request, f'Автопродление {status}.')
    return redirect('subscriptions:my_subscription')
