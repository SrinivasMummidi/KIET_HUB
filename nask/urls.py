from django.urls import path
from .views import TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView, ResponseListView
from . import views as nask_views



urlpatterns = [
    path('', nask_views.home, name="Kiet-Home"),
    path('tasks/', TaskListView.as_view(), name="Tasks"),
    path('tasks/<int:pk>/', nask_views.TaskDetailView, name="task-detail"),
    path('tasks/new/', TaskCreateView.as_view(), name="task-create"),
    path('tasks/<int:pk>/update', TaskUpdateView.as_view(), name="task-update"),
    path('tasks/<int:pk>/delete', TaskDeleteView.as_view(), name="task-delete"),
    path('tasks/<int:pk>/responses', nask_views.ResponseListView, name="task-responses"),
]
