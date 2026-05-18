from django.urls import path
from . import views

app_name = 'interactions'

urlpatterns = [
    path('comment/add/', views.add_comment, name='add_comment'),
    path('comment/delete/', views.delete_comment, name='delete_comment'),
    path('like/toggle/', views.toggle_like, name='toggle_like'),
    path('bookmark/toggle/', views.toggle_bookmark, name='toggle_bookmark'),
    path('bookmarks/', views.bookmarks_list, name='bookmarks_list'),
]
