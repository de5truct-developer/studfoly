from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.inbox_view, name='inbox'),
    path('conversation/<int:conversation_id>/', views.conversation_view, name='conversation'),
    path('start/<str:username>/', views.start_conversation, name='start_conversation'),
    path('send/', views.send_message, name='send_message'),
    path('check-new/', views.check_new_messages, name='check_new_messages'),
    path('unread-count/', views.unread_count, name='unread_count'),
]
