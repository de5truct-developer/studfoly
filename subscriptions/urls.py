from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('plans/', views.plans_view, name='plans'),
    path('checkout/<str:plan_name>/', views.checkout_view, name='checkout'),
    path('checkout/<str:plan_name>/<str:period>/', views.checkout_view, name='checkout_period'),
    path('process-payment/', views.process_payment_view, name='process_payment'),
    path('my-subscription/', views.my_subscription_view, name='my_subscription'),
    path('cancel/', views.cancel_subscription_view, name='cancel'),
    path('toggle-auto-renew/', views.toggle_auto_renew_view, name='toggle_auto_renew'),
]
