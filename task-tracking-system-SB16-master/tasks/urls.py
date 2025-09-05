from django.urls import path
from tasks import views

urlpatterns = [
    path("", views.TaskListView.as_view(), name="task-list"),
    path("<int:pk>/", views.TaskDetailView.as_view(), name="task-detail"),
    path("<int:pk>/update/", views.TaskUpdateView.as_view(), name="task-update"),
    path("<int:pk>/delete/", views.TaskDeleteView.as_view(), name="task-delete"),
    path("create-task/", views.TaskCreateView.as_view(), name="task-create"),

    # path for comments
    path("<int:pk>/comment-edit/", views.CommentEditView.as_view(), name="comment-edit"),
    path("<int:pk>/comment-delete/", views.CommentDeleteView.as_view(), name="comment-delete"),
]