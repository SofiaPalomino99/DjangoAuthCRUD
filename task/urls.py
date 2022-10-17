from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('signup/', views.signup, name = 'signup'),
    path('task/', views.task, name = 'task'),
    path('logout/', views.signout, name = 'logout'),
    path('signin/', views.signin, name = 'signin'),
    path('task/create/', views.create_task, name = 'create_task'),
    path('task/<int:task_id>/complete/', views.complete_task, name = 'complete_task'),
    path('task/<int:task_id>/', views.task_detail, name = 'task_detail'),
    path('task/<int:task_id>/delete', views.delete_task, name = 'delete_task'),
    path('task_completed/', views.task_completed, name = 'task_completed'),
]
