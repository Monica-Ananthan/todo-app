from django.contrib import admin
from django.urls import path
from todo_app import views

urlpatterns = [
    path('test/', views.test, name="test"),
    path('', views.index, name="index"),
    path('add/', views.add_task, name='add_task'),
    path('toggle/<int:task_id>/', views.toggle_task, name='toggle_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('update/<int:task_id>/', views.update_task, name='update_task'),
    path('add-category/', views.add_category, name='add_category'),
    path('delete-category/<int:id>/', views.delete_category, name='delete_category'),
    path('categories/', views.category_list_partial, name='category_list_partial'),
    
]