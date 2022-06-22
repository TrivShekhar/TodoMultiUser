from django.urls import path
from .views import TaskCreateView, TaskDelete, TaskListView, TaskDetailView, TaskUpdate, UserLoginView, UserRegisterView
from django.contrib.auth.views import LogoutView
urlpatterns=[
    path('login/',UserLoginView.as_view(),name="login"),
    path('register/',UserRegisterView.as_view(),name="register"),
    path('logout/',LogoutView.as_view(next_page="login"),name='logout'),
    path('',TaskListView.as_view(),name="tasklist"),
    path('task/<int:pk>/',TaskDetailView.as_view(),name="task"),
    path('createTask/',TaskCreateView.as_view(),name="createTask"),
    path('editTask/<int:pk>/',TaskUpdate.as_view(),name="edittask"),
    path('deleteTask/<int:pk>/',TaskDelete.as_view(),name="deletetask"),
    
    ]