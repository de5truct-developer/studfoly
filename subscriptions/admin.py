from django.contrib import admin
from .models import SubscriptionPlan, UserSubscription, Payment


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'name', 'price_monthly', 'price_yearly', 'max_projects', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active',)


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'status', 'period', 'start_date', 'end_date', 'auto_renew')
    list_filter = ('status', 'period', 'plan')
    search_fields = ('user__username', 'user__email')
    raw_id_fields = ('user',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'plan', 'amount', 'status', 'payment_method', 'created_at')
    list_filter = ('status', 'payment_method', 'plan')
    search_fields = ('user__username', 'transaction_id')
    raw_id_fields = ('user',)
    readonly_fields = ('transaction_id', 'completed_at')
